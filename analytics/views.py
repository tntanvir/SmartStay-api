from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authsystem.models import CustomUser
from room.models import RoomModel
from booking.models import BookingModel




class AnaliticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()
        today = now.date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        # === Base QuerySets depending on role ===
        if user.is_superuser or user.role == "admin":  # Admin → all data
            users_qs = CustomUser.objects.all()
            rooms_qs = RoomModel.objects.all()
            bookings_qs = BookingModel.objects.all()

        elif user.role == "hotel owner":  # Owner → only his rooms & bookings
            rooms_qs = RoomModel.objects.filter(user=user)
            bookings_qs = BookingModel.objects.filter(room__user=user)
            users_qs = CustomUser.objects.filter(
                id__in=bookings_qs.values_list("user_id", flat=True)
            )

        else:  # Normal User → only his bookings
            bookings_qs = BookingModel.objects.filter(user=user)
            rooms_qs = RoomModel.objects.filter(
                id__in=bookings_qs.values_list("room_id", flat=True)
            )
            users_qs = CustomUser.objects.filter(id=user.id)

        # === Totals ===
        total_users = users_qs.count()
        total_rooms = rooms_qs.count()
        total_bookings = bookings_qs.count()

        # === Helper function for counts ===
        def get_counts(qs, date_filter=None):
            filtered = qs
            if date_filter:
                filtered = qs.filter(updated_at__date__gte=date_filter)

            return {
                "paid": filtered.filter(payment_status="paid").count(),
                "unpaid": filtered.filter(payment_status="unpaid").count(),
                "confirmed": filtered.filter(status="confirmed").count(),
                "cancelled": filtered.filter(status="cancelled").count(),
                "completed_checkouts": filtered.filter(
                    end_date__lt=today, status="confirmed"
                ).count(),
            }

        # === Timeframe Counts ===
        today_data = {
            "new_users": users_qs.filter(date_joined__date=today).count(),
            "new_rooms": rooms_qs.filter(created_at__date=today).count(),
            "new_bookings": bookings_qs.filter(created_at__date=today).count(),
            "booking_statuses": get_counts(
                bookings_qs.filter(updated_at__date=today)
            ),
        }

        week_data = {
            "new_users": users_qs.filter(date_joined__date__gte=start_of_week).count(),
            "new_rooms": rooms_qs.filter(created_at__date__gte=start_of_week).count(),
            "new_bookings": bookings_qs.filter(created_at__date__gte=start_of_week).count(),
            "booking_statuses": get_counts(bookings_qs, start_of_week),
        }

        month_data = {
            "new_users": users_qs.filter(date_joined__date__gte=start_of_month).count(),
            "new_rooms": rooms_qs.filter(created_at__date__gte=start_of_month).count(),
            "new_bookings": bookings_qs.filter(created_at__date__gte=start_of_month).count(),
            "booking_statuses": get_counts(bookings_qs, start_of_month),
        }

        year_data = {
            "new_users": users_qs.filter(date_joined__date__gte=start_of_year).count(),
            "new_rooms": rooms_qs.filter(created_at__date__gte=start_of_year).count(),
            "new_bookings": bookings_qs.filter(created_at__date__gte=start_of_year).count(),
            "booking_statuses": get_counts(bookings_qs, start_of_year),
        }

        # === Booking Status Totals ===
        booking_statuses_total = get_counts(bookings_qs)

        # === Top Rooms === (only for admin & owner)
        top_rooms = []
        if user.is_superuser or user.role in ["admin", "hotel owner"]:
            top_rooms = (
                bookings_qs.values("room__id", "room__title")
                .annotate(total_bookings=Count("id"))
                .order_by("-total_bookings")[:5]
            )

        # === Top Users === (only for admin & owner)
        top_users = []
        if user.is_superuser or user.role in ["admin", "hotel owner"]:
            top_users = (
                bookings_qs.values("user__id", "user__username")
                .annotate(total_bookings=Count("id"))
                .order_by("-total_bookings")[:5]
            )

        # === Final Response ===
        data = {
            "totals": {
                "users": total_users,
                "rooms": total_rooms,
                "bookings": total_bookings,
            },
            "today": today_data,
            "this_week": week_data,
            "this_month": month_data,
            "this_year": year_data,
            "booking_statuses_total": booking_statuses_total,
            "top_rooms": list(top_rooms),
            "top_users": list(top_users),
        }

        return Response(data, status=status.HTTP_200_OK)

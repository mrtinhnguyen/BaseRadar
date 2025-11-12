"""
Date Parsing Tool

Supports parsing multiple natural language date formats, including relative and absolute dates.
"""

import re
from datetime import datetime, timedelta

from .errors import InvalidParameterError


class DateParser:
    """Date parser class"""

    # Chinese date mapping
    CN_DATE_MAPPING = {
        "今天": 0,
        "昨天": 1,
        "前天": 2,
        "大前天": 3,
    }

    # English date mapping
    EN_DATE_MAPPING = {
        "today": 0,
        "yesterday": 1,
    }

    # Weekday mapping
    WEEKDAY_CN = {
        "一": 0, "二": 1, "三": 2, "四": 3,
        "五": 4, "六": 5, "日": 6, "天": 6
    }

    WEEKDAY_EN = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }

    @staticmethod
    def parse_date_query(date_query: str) -> datetime:
        """
        Parse date query string

        Supported formats:
        - Relative dates (Chinese): 今天 (today), 昨天 (yesterday), 前天 (day before yesterday), 大前天 (3 days ago), N天前 (N days ago)
        - Relative dates (English): today, yesterday, N days ago
        - Weekdays (Chinese): 上周一 (last monday), 上周二 (last tuesday), 本周三 (this wednesday)
        - Weekdays (English): last monday, this friday
        - Absolute dates: 2025-10-10, 10月10日 (October 10), 2025年10月10日 (October 10, 2025)

        Args:
            date_query: Date query string

        Returns:
            datetime object

        Raises:
            InvalidParameterError: Date format unrecognized

        Examples:
            >>> DateParser.parse_date_query("today")
            datetime(2025, 10, 11)
            >>> DateParser.parse_date_query("yesterday")
            datetime(2025, 10, 10)
            >>> DateParser.parse_date_query("3 days ago")
            datetime(2025, 10, 8)
            >>> DateParser.parse_date_query("2025-10-10")
            datetime(2025, 10, 10)
        """
        if not date_query or not isinstance(date_query, str):
            raise InvalidParameterError(
                "Date query string cannot be empty",
                suggestion="Please provide a valid date query, e.g.: today, yesterday, 2025-10-10"
            )

        date_query = date_query.strip().lower()

        # 1. Try to parse Chinese common relative dates
        if date_query in DateParser.CN_DATE_MAPPING:
            days_ago = DateParser.CN_DATE_MAPPING[date_query]
            return datetime.now() - timedelta(days=days_ago)

        # 2. Try to parse English common relative dates
        if date_query in DateParser.EN_DATE_MAPPING:
            days_ago = DateParser.EN_DATE_MAPPING[date_query]
            return datetime.now() - timedelta(days=days_ago)

        # 3. Try to parse "N days ago" (Chinese: "N天前") or "N days ago" (English)
        cn_days_ago_match = re.match(r'(\d+)\s*天前', date_query)
        if cn_days_ago_match:
            days = int(cn_days_ago_match.group(1))
            if days > 365:
                raise InvalidParameterError(
                    f"Days too large: {days} days",
                    suggestion="Please use relative dates less than 365 days or use absolute dates"
                )
            return datetime.now() - timedelta(days=days)

        en_days_ago_match = re.match(r'(\d+)\s*days?\s+ago', date_query)
        if en_days_ago_match:
            days = int(en_days_ago_match.group(1))
            if days > 365:
                raise InvalidParameterError(
                    f"Days too large: {days} days",
                    suggestion="Please use relative dates less than 365 days or use absolute dates"
                )
            return datetime.now() - timedelta(days=days)

        # 4. Try to parse weekdays (Chinese: "上周一", "本周三" meaning "last Monday", "this Wednesday")
        cn_weekday_match = re.match(r'(上|本)周([一二三四五六日天])', date_query)
        if cn_weekday_match:
            week_type = cn_weekday_match.group(1)  # "上" (last) or "本" (this)
            weekday_str = cn_weekday_match.group(2)
            target_weekday = DateParser.WEEKDAY_CN[weekday_str]
            return DateParser._get_date_by_weekday(target_weekday, week_type == "上")

        # 5. Try to parse weekdays (English): last monday, this friday
        en_weekday_match = re.match(r'(last|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', date_query)
        if en_weekday_match:
            week_type = en_weekday_match.group(1)  # last or this
            weekday_str = en_weekday_match.group(2)
            target_weekday = DateParser.WEEKDAY_EN[weekday_str]
            return DateParser._get_date_by_weekday(target_weekday, week_type == "last")

        # 6. Try to parse absolute date: YYYY-MM-DD
        iso_date_match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_query)
        if iso_date_match:
            year = int(iso_date_match.group(1))
            month = int(iso_date_match.group(2))
            day = int(iso_date_match.group(3))
            try:
                return datetime(year, month, day)
            except ValueError as e:
                raise InvalidParameterError(
                    f"Invalid date: {date_query}",
                    suggestion=f"Date value error: {str(e)}"
                )

        # 7. Try to parse Chinese date format: MM月DD日 or YYYY年MM月DD日 (e.g., "10月10日" or "2025年10月10日")
        cn_date_match = re.match(r'(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日', date_query)
        if cn_date_match:
            year_str = cn_date_match.group(1)
            month = int(cn_date_match.group(2))
            day = int(cn_date_match.group(3))

            # If no year, use current year
            if year_str:
                year = int(year_str)
            else:
                year = datetime.now().year
                # If month is greater than current month, it's last year
                current_month = datetime.now().month
                if month > current_month:
                    year -= 1

            try:
                return datetime(year, month, day)
            except ValueError as e:
                raise InvalidParameterError(
                    f"Invalid date: {date_query}",
                    suggestion=f"Date value error: {str(e)}"
                )

        # 8. Try to parse slash format: YYYY/MM/DD or MM/DD
        slash_date_match = re.match(r'(?:(\d{4})/)?(\d{1,2})/(\d{1,2})', date_query)
        if slash_date_match:
            year_str = slash_date_match.group(1)
            month = int(slash_date_match.group(2))
            day = int(slash_date_match.group(3))

            if year_str:
                year = int(year_str)
            else:
                year = datetime.now().year
                current_month = datetime.now().month
                if month > current_month:
                    year -= 1

            try:
                return datetime(year, month, day)
            except ValueError as e:
                raise InvalidParameterError(
                    f"Invalid date: {date_query}",
                    suggestion=f"Date value error: {str(e)}"
                )

        # If all formats don't match
        raise InvalidParameterError(
            f"Unrecognized date format: {date_query}",
            suggestion=(
                "Supported formats:\n"
                "- Relative dates: 今天 (today), 昨天 (yesterday), 前天 (day before yesterday), 3天前 (3 days ago), today, yesterday, 3 days ago\n"
                "- Weekdays: 上周一 (last monday), 本周三 (this wednesday), last monday, this friday\n"
                "- Absolute dates: 2025-10-10, 10月10日 (October 10), 2025年10月10日 (October 10, 2025)"
            )
        )

    @staticmethod
    def _get_date_by_weekday(target_weekday: int, is_last_week: bool) -> datetime:
        """
        Get date by weekday

        Args:
            target_weekday: Target weekday (0=Monday, 6=Sunday)
            is_last_week: Whether it's last week

        Returns:
            datetime object
        """
        today = datetime.now()
        current_weekday = today.weekday()

        # Calculate days difference
        if is_last_week:
            # A day in last week
            days_diff = current_weekday - target_weekday + 7
        else:
            # A day in this week
            days_diff = current_weekday - target_weekday
            if days_diff < 0:
                days_diff += 7

        return today - timedelta(days=days_diff)

    @staticmethod
    def format_date_folder(date: datetime) -> str:
        """
        Format date as folder name

        Args:
            date: datetime object

        Returns:
            Folder name, format: YYYY-MM-DD

        Examples:
            >>> DateParser.format_date_folder(datetime(2025, 10, 11))
            '2025-10-11'
        """
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def validate_date_not_future(date: datetime) -> None:
        """
        Validate date is not in the future

        Args:
            date: Date to validate

        Raises:
            InvalidParameterError: Date is in the future
        """
        if date.date() > datetime.now().date():
            raise InvalidParameterError(
                f"Cannot query future date: {date.strftime('%Y-%m-%d')}",
                suggestion="Please use today or past dates"
            )

    @staticmethod
    def validate_date_not_too_old(date: datetime, max_days: int = 365) -> None:
        """
        Validate date is not too old

        Args:
            date: Date to validate
            max_days: Maximum days

        Raises:
            InvalidParameterError: Date is too old
        """
        days_ago = (datetime.now().date() - date.date()).days
        if days_ago > max_days:
            raise InvalidParameterError(
                f"Date is too old: {date.strftime('%Y-%m-%d')} ({days_ago} days ago)",
                suggestion=f"Please query data within {max_days} days"
            )

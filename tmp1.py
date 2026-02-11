def attendance_summary_WAIT(request):
    company_id = request.COOKIES.get("company_id")
    staff_list = Staff.objects.filter(company_id=company_id, discontinued=0)

    staff_id = request.GET.get("staff")
    month_str = request.GET.get("month") or timezone.now().strftime("%Y-%m")

    try:
        dt = datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        dt = timezone.now()

    today = date.today()

    context = {
        "staff_list": staff_list,
        "month_input": dt.strftime("%Y-%m"),
        "records": [],
        "gross_salary": 0,
        "credit_total": 0,
        "net_salary": 0,
        "salary_value": 0,
        "working_days": 0,
        "credits": [],
        "today": today.isoformat(),
    }

    if not staff_id:
        return render(request, "attendance_summary.html", context)

    data = staff_salary(staff_id, dt.strftime("%Y%m"))
    if not data:
        return render(request, "attendance_summary.html", context)

    # === Load Approved Leaves ===
    leave_qs = StaffLeave.objects.filter(
        staff_id=staff_id,
        status="APPROVED",
        leave_date__range=[data["start_date"], data["end_date"]],
    )

    leave_map = {}  # {date: "APPROVED FULL" or set(["MORNING", "AFTERNOON"])}
    for lv in leave_qs:
        lt = lv.leave_type.upper()
        if lt == "FULL":
            leave_map[lv.leave_date] = "APPROVED FULL"
        elif lt == "HALF_MORNING":
            leave_map.setdefault(lv.leave_date, set()).add("MORNING")
        elif lt == "HALF_AFTERNOON":
            leave_map.setdefault(lv.leave_date, set()).add("AFTERNOON")

    # === Generate Daily Records ===
    daily_records = []
    for day in range(1, data["loop_end_day"] + 1):
        current_date = data["dt"].replace(day=day).date()
        entry = data["attendance_map"].get(current_date)

        record = {
            "date": current_date,
            "in_time": None,
            "out_time": None,
            "status": "ABSENT",
            "amount": 0,
        }

        leave_status = leave_map.get(current_date)
        approved_incentive = int(request.setting_value("staff_approved_leave_incentive") or 0)
        if leave_status:
            if leave_status == "APPROVED FULL":
                record["status"] = "APPROVED FULL"
                record["amount"] = approved_incentive  #  fixed amount from setting
            elif isinstance(leave_status, set):
                if "MORNING" in leave_status and "AFTERNOON" in leave_status:
                    record["status"] = "APPROVED FULL"
                    record["amount"] = approved_incentive  #  fixed amount from setting
                elif "MORNING" in leave_status:
                    record["status"] = "APPROVED MORNING"
                    record["amount"] = approved_incentive / 2  #  half of the incentive
                elif "AFTERNOON" in leave_status:
                    record["status"] = "APPROVED AFTERNOON"
                    record["amount"] = approved_incentive / 2  #  half of the incentive


        elif entry and entry.in_time and entry.out_time:
            in_time_obj = get_ist_time_from_unix(entry.in_time)
            out_time_obj = get_ist_time_from_unix(entry.out_time)

            record["in_time"] = in_time_obj.strftime("%I:%M:%S %p")
            record["out_time"] = out_time_obj.strftime("%I:%M:%S %p")

            late = in_time_obj.time() > time(10, 0)
            early = out_time_obj.time() < time(20, 0)

            if late or early:
                record["status"] = "H"
                record["amount"] = data["full_day_salary"] / 2
            else:
                record["status"] = "F"
                record["amount"] = data["full_day_salary"]
        else:
            # No attendance and no approved leave → unapproved leave
            record["status"] = "UNAPPROVED"
            record["amount"] = 0

        daily_records.append(record)

    # === Credit Details ===
    credit_qs = Staff_Credit.objects.filter(
        staff=data["staff"],
        date__range=[data["start_date"], data["end_date"]],
    )

    # === Incentive / Penalty Settings ===
    approved_incentive = int(request.setting_value("staff_approved_leave_incentive") or 0)
    unapproved_penalty = int(request.setting_value("staff_unapproved_leave_penalty") or 0)

    approved_count = sum(1 for r in daily_records if r["status"] in ["APPROVED FULL", "APPROVED MORNING", "APPROVED AFTERNOON"])
    unapproved_count = sum(1 for r in daily_records if r["status"] == "UNAPPROVED")

    total_incentive = approved_count * approved_incentive
    total_penalty = unapproved_count * unapproved_penalty

    final_salary = data["net_salary"] + total_incentive - total_penalty

    context.update({
        "staff": data["staff"],
        "records": daily_records,
        "gross_salary": data["gross_salary"],
        "credit_total": data["credit_total"],
        "net_salary": data["net_salary"],
        "salary_value": data["monthly_salary"],
        "working_days": data["working_days"],
        "credits": credit_qs,
        "approved_leave_count": approved_count,
        "unapproved_leave_count": unapproved_count,
        "approved_incentive": total_incentive,
        "unapproved_penalty": total_penalty,
        "final_salary": final_salary,
    })

    return render(request, "attendance_summary.html", context)


def attendance_summary_RECENT(request):
    company_id = request.COOKIES.get("company_id")
    staff_list = Staff.objects.filter(company_id=company_id, discontinued=0)

    staff_id = request.GET.get("staff")
    month_str = request.GET.get("month") or timezone.now().strftime("%Y-%m")

    try:
        dt = datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        dt = timezone.now()

    today = date.today()

    context = {
        "staff_list": staff_list,
        "month_input": dt.strftime("%Y-%m"),
        "records": [],
        "gross_salary": 0,
        "credit_total": 0,
        "net_salary": 0,
        "salary_value": 0,
        "working_days": 0,
        "credits": [],
        "today": today.isoformat(),
    }

    if not staff_id:
        return render(request, "attendance_summary.html", context)



    data = staff_salary(staff_id, dt.strftime("%Y%m"))
    if not data:
        return render(request, "attendance_summary.html", context)

    # === Load Approved Leaves ===
    leave_qs = StaffLeave.objects.filter(
        staff_id=staff_id,
        status="APPROVED",
        leave_date__range=[data["start_date"], data["end_date"]],
    )

    leave_map = {}  # {date: "APPROVED FULL" or set(["MORNING", "AFTERNOON"])}
    for lv in leave_qs:
        lt = lv.leave_type.upper()
        if lt == "FULL":
            leave_map[lv.leave_date] = "APPROVED FULL"
        elif lt == "HALF_MORNING":
            leave_map.setdefault(lv.leave_date, set()).add("MORNING")
        elif lt == "HALF_AFTERNOON":
            leave_map.setdefault(lv.leave_date, set()).add("AFTERNOON")

    # === Generate Daily Records ===
    daily_records = []
    for day in range(1, data["loop_end_day"] + 1):
        current_date = data["dt"].replace(day=day).date()
        entry = data["attendance_map"].get(current_date)

        record = {
            "date": current_date,
            "in_time": None,
            "out_time": None,
            "status": "ABSENT",
            "amount": 0,
        }

        leave_status = leave_map.get(current_date)

        if leave_status:
            if leave_status == "APPROVED FULL":
                record["status"] = "APPROVED FULL"
                record["amount"] = data["full_day_salary"]
            elif isinstance(leave_status, set):
                if "MORNING" in leave_status and "AFTERNOON" in leave_status:
                    record["status"] = "APPROVED FULL"
                    record["amount"] = data["full_day_salary"]
                elif "MORNING" in leave_status:
                    record["status"] = "APPROVED MORNING"
                    record["amount"] = data["full_day_salary"] / 2
                elif "AFTERNOON" in leave_status:
                    record["status"] = "APPROVED AFTERNOON"
                    record["amount"] = data["full_day_salary"] / 2

        elif entry and entry.in_time and entry.out_time:
            in_time_obj = get_ist_time_from_unix(entry.in_time)
            out_time_obj = get_ist_time_from_unix(entry.out_time)

            record["in_time"] = in_time_obj.strftime("%I:%M:%S %p")
            record["out_time"] = out_time_obj.strftime("%I:%M:%S %p")

            late = in_time_obj.time() > time(10, 0)
            early = out_time_obj.time() < time(20, 0)

            if late or early:
                record["status"] = "H"
                record["amount"] = data["full_day_salary"] / 2
            else:
                record["status"] = "F"
                record["amount"] = data["full_day_salary"]

        daily_records.append(record)

    # === Credit Details ===
    credit_qs = Staff_Credit.objects.filter(
        staff=data["staff"],
        date__range=[data["start_date"], data["end_date"]],
    )

    context.update({
        "staff": data["staff"],
        "records": daily_records,
        "gross_salary": data["gross_salary"],
        "credit_total": data["credit_total"],
        "net_salary": data["net_salary"],
        "salary_value": data["monthly_salary"],
        "working_days": data["working_days"],
        "credits": credit_qs,
    })

    return render(request, "attendance_summary.html", context)

def attendance_summary_OLD(request):
    company_id = request.COOKIES.get("company_id")
    staff_list = Staff.objects.filter(company_id=company_id, discontinued=0)

    staff_id = request.GET.get("staff")
    month_str = request.GET.get("month") or timezone.now().strftime("%Y-%m")

    try:
        dt = datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        dt = timezone.now()

    today = date.today()

    context = {
        "staff_list": staff_list,
        "month_input": dt.strftime("%Y-%m"),
        "records": [],
        "gross_salary": 0,
        "credit_total": 0,
        "net_salary": 0,
        "salary_value": 0,
        "working_days": 0,
        "credits": [],
        "today": today.isoformat(),
    }

    if not staff_id:
        return render(request, "attendance_summary.html", context)

    data = staff_salary(staff_id, dt.strftime("%Y%m"))
    if not data:
        return render(request, "attendance_summary.html", context)

    daily_records = []
    for day in range(1, data["loop_end_day"] + 1):
        current_date = data["dt"].replace(day=day).date()
        entry = data["attendance_map"].get(current_date)

        record = {
            "date": current_date,
            "in_time": None,
            "out_time": None,
            "status": "ABSENT",
            "amount": 0,
        }

        if entry and entry.in_time and entry.out_time:
            in_time_obj = get_ist_time_from_unix(entry.in_time)
            out_time_obj = get_ist_time_from_unix(entry.out_time)

            record["in_time"] = in_time_obj.strftime("%I:%M:%S %p")
            record["out_time"] = out_time_obj.strftime("%I:%M:%S %p")

            late = in_time_obj.time() > time(10, 0)
            early = out_time_obj.time() < time(20, 0)

            if late or early:
                record["status"] = "H"
                record["amount"] = data["full_day_salary"] / 2
            else:
                record["status"] = "F"
                record["amount"] = data["full_day_salary"]
        elif entry:
            # record["status"] = "H"
            # record["amount"] = data["full_day_salary"] / 2
            pass

        daily_records.append(record)

    credit_qs = Staff_Credit.objects.filter(staff=data["staff"], date__range=[data["start_date"], data["end_date"]])

    context.update({


        "staff": data["staff"],
        "records": daily_records,
        "gross_salary": data["gross_salary"],
        "credit_total": data["credit_total"],
        "net_salary": data["net_salary"],
        "salary_value": data["monthly_salary"],
        "working_days": data["working_days"],
        "credits": credit_qs,
    })


    return render(request, "attendance_summary.html", context)

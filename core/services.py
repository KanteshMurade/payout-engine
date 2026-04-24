def update_status(payout, new_status):
    valid = {
        "pending": ["processing"],
        "processing": ["completed", "failed"],
    }

    if new_status not in valid.get(payout.status, []):
        raise Exception("Invalid state transition")

    payout.status = new_status
    payout.save()
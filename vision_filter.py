from config import MIN_CONFIDENCE


def verify_scene(candidate):

    if not candidate.get("is_live"):
        return False

    if candidate.get("is_split_screen"):
        return False

    if candidate.get("is_video_call"):
        return False

    if candidate.get("shown_on_screen"):
        return False

    if not candidate.get("same_physical_scene"):
        return False

    if not candidate.get("man_and_woman"):
        return False

    confidence = float(candidate.get("confidence", 0))

    if confidence < MIN_CONFIDENCE:
        return False

    return True


def filter_candidates(candidates):

    confirmed = []

    for candidate in candidates:

        if verify_scene(candidate):
            confirmed.append(candidate)

    return confirmed

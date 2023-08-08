import math


def pagination(form, page, limit):
    return {
        "current_page": page,
        "limit": limit,
        "pages": math.ceil(form.count() / limit),
        "data": form.offset((page) * limit).limit(limit).all()
    }

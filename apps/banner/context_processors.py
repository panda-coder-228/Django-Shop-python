from django.core.cache import cache

from apps.banner.models import MainBanner


def banner(request):
    main_banner = cache.get("main_banner")

    if main_banner is None:
        main_banner = (
            MainBanner.objects
            .filter(is_active=True)
            .first()
        )

        cache.set(
            "main_banner",
            main_banner,
            60 * 15  # 15 минут
        )

    return {
        "main_banner": main_banner
    }
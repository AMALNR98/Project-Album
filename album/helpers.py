def parse_id_from_slug(slug: str) -> int:
    '''get id from slug'''
    try:
        return int(slug.split('-')[-1])
    except Exception as e:
        print(e)
        return 0
    
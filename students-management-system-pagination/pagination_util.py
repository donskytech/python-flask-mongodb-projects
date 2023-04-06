def generate_pagination_query(query, sort=None, next_key=None, previous_navigation=False):
    sort_field = None if sort is None else sort[0]

    def next_key_fn(items, previous_item=False):
        if len(items) == 0:
            return None
        index = -1 if not previous_item else 0
        next_item = items[index]
        if sort_field is None:
            return {'_id': next_item['_id']}
        else:
            return {'_id': next_item['_id'], sort_field: next_item[sort_field]}

    if next_key is None:
        return query, next_key_fn

    paginated_query = query.copy()

    if sort is None:
        paginated_query['_id'] = {'$gt': next_key['_id']}
        return paginated_query, next_key_fn

    sort_operator = '$gt' if sort[1] == 1 else '$lt'
    if previous_navigation:
        sort_operator = '$gte' if sort[1] == 1 else '$lte'

    pagination_query = [
        {sort_field: {sort_operator: next_key[sort_field]}},
        {'$and': [
            {sort_field: next_key[sort_field]},
            {'_id': {sort_operator: next_key['_id']}},
        ]},
    ]

    if '$or' not in paginated_query:
        paginated_query['$or'] = pagination_query
    else:
        paginated_query = {'$and': [query, {'$or': pagination_query}]}

    return paginated_query, next_key_fn
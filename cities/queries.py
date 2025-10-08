city_cache = {
    
}

def create(data, dict):
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(NAME):
        raise ValueError(f'Bad type for {data.get(NAME)=}')
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = data
    return new_id

def num_cities():
    return len(city_cache)


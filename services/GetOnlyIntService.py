class GetOnlyIntFromListService: 
    def clear(lst: list[str | int]) -> list[int]: 
        return [val for val in lst if isinstance(val, int)]
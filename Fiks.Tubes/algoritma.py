from database_konten import database

def sequential_search(data, keyword):
    arr = []
    target = 'hashtags' if keyword.startswith('#') else 'judul'
    for item in data:
        if keyword.lower() in item[target].lower():
            arr.append(item)
    return arr

def selection_sort(data, key):
    """Ascending sort menggunakan Selection Sort."""
    n = len(data)
    arr = data.copy()
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j][key] < arr[min_index][key]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def insertion_sort(data, key):
    """Descending sort menggunakan Insertion Sort."""
    arr = data.copy()
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] < current[key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

def sort_data(data, key, reverse=False):
    """
    Dispatcher sort:
    - reverse=False (ascending)  → Selection Sort
    - reverse=True  (descending) → Insertion Sort
    """
    if reverse:
        return insertion_sort(data, key)
    else:
        return selection_sort(data, key)

def filter_by_category(data, category):
    hasil = []
    for item in data:
        if category.lower() in item['category'].lower():
            hasil.append(item)
    return hasil

def binary_search(data, keyword):
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid]['id'] == keyword:
            return mid
        elif data[mid]['id'] < keyword:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def find_index_by_id(data, id):
    """Sequential search by ID"""
    for i, item in enumerate(data):
        if item['id'] == id:
            return i
    return -1

def update_content(data, id, new_data):
    index = find_index_by_id(data, id)
    if index != -1:
        data[index].update(new_data)
        return True
    return False

def delete_content(data, id):
    index = find_index_by_id(data, id)
    if index != -1:
        del data[index]
        return True
    return False

def insert_content(data, new_item: dict):
    """Sisipkan konten baru. Menerima dict lengkap dari main.py."""
    next_id = (data[-1]['id'] + 1) if data else 1
    new_item['id'] = next_id
    data.append(new_item)
    return True

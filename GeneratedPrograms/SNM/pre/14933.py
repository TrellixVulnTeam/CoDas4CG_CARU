for _ in range(int(input())):
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    count = 0
    for i in range(n):
        if arr[i] == arr[i]:
            count += 1
    print(count)
    print('YES')

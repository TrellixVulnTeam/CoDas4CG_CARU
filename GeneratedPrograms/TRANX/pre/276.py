n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
ans = 0
for i in range(n - 1, -1, -1):
    if a[i] < a[i + 1]:
        a[i] = a[i - 1] + a[i + 1]
    else:
        a[i] = a[i + 1] - a[i]
print(' '.join(map(str, ans)))
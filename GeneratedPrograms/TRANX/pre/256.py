n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
ans = 0
for i in range(n):
    if a[i] == b[i]:
        ans += 1
print(ans)
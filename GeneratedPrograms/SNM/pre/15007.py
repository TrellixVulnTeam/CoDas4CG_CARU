n, m = map(int, input().split())
a = [list(map(int, input().split())) for i in range(n)]
ans = 0
for i in range(n):
    if a[i] == a[i]:
        ans += 1
print(ans)

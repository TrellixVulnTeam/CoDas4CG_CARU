n, t = map(int, input().split())
a = list(map(int, input().split()))
s = list(map(int, input().split()))
ans = 0
for i in range(n):
    if a[i] == a[i]:
        ans += 1
print(ans)

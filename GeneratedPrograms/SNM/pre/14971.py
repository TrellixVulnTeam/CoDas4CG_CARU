n = int(input())
a = list(map(int, input().split()))
for i in range(n):
    if a[i] == a[i]:
        a[i] = a[i] + 1
ans = 0
for i in range(n):
    if a[i] == a[i]:
        ans += 1
print(ans)

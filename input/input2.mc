int max(int a, int b) {
if (a > b) {
return a;
} else {
return b;
}
}

int main() {
int x = 10;
int y = 5;
int m = max(x, y);
if (m == x) {
printf("x is max\n");
} else {
printf("y is max\n");
}
return 0;
}
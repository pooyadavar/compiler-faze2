int func1(int a, int b) {
    if ((a > b))
    {
        return a;
    }
    else
    {
        return b;
    }
}
int main() {
    int x;
    int y;
    int m;
    x = 10;
    y = 5;
    m = func1(x, y);
    if ((!(m != x)))
    {
        printf("x is max\n");
    }
    else
    {
        printf("y is max\n");
    }
    return 0;
}
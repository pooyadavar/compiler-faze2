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
    int y;
    int m;
    int n;
    y = 10;
    m = 5;
    n = func1(y, m);
    if ((!(n != y)))
    {
        printf("x is max\n");
    }
    else
    {
        printf("y is max\n");
    }
    return 0;
}
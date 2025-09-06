

int add(int a, int b) {
    int result = a + b;
    return result;
}

int main() {
    int x = 5;
    int y = 10;
    int sum = add(x, y);
    printf("%d\n", sum);

    while(x==5){
        printf("sample");
    }
    int i = 0;
    for (; i < 5; i = i + 1) {
        printf("i is %d\n", i);
    }
    return 0;
}

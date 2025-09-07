int func1(int a, int b) {
    int x = 0;
_f0_dispatcher:
    switch (x) {
        case 0: goto case_0;
        case 1: goto case_1;
    }
    {
    _f0_case_0:
        if ((a > b))
        {
            if (0)
            {
                printf("Unreachable\\n");
            }
            return a;
        }
        else
        {
            return b;
        }
        x = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int x = 0;
    int y;
    int m;
    int n;
_f1_dispatcher:
    switch (x) {
        case 0: goto case_0;
        case 1: goto case_1;
        case 2: goto case_2;
        case 3: goto case_3;
        case 4: goto case_4;
        case 5: goto case_5;
        case 6: goto case_6;
        case 7: goto case_7;
    }
    {
    _f1_case_0:
        if (0)
        {
            printf("Unreachable\\n");
        }
        x = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        y = 10;
        x = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        m = 5;
        x = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        n = func1(y, m);
        x = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        if ((!(n != y)))
        {
            printf("x is max\n");
        }
        else
        {
            printf("y is max\n");
        }
        x = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        if (0)
        {
            printf("Unreachable\\n");
        }
        x = 6;
        goto _f1_dispatcher;
    }
    {
    _f1_case_6:
        return 0;
    }
    {
    _f1_end:
        return 0;
    }
}
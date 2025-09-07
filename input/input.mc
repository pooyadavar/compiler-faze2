int cxq826(int yjv219, int dpc128) {
    int _f0_state = 0;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_end;
    }
    {
    _f0_case_0:
        if ((yjv219 > dpc128))
        {
            if (0)
            {
                printf("Unreachable\\n");
            }
            return yjv219;
        }
        else
        {
            return dpc128;
        }
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int orz404;
    int xfz533;
    int ysl423;
_f1_dispatcher:
    switch (_f1_state) {
        case 0: goto _f1_case_0;
        case 1: goto _f1_case_1;
        case 2: goto _f1_case_2;
        case 3: goto _f1_case_3;
        case 4: goto _f1_case_4;
        case 5: goto _f1_case_5;
        case 6: goto _f1_case_6;
        case 7: goto _f1_end;
    }
    {
    _f1_case_0:
        if (0)
        {
            printf("Unreachable\\n");
        }
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        orz404 = 10;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        xfz533 = 5;
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        ysl423 = cxq826(orz404, xfz533);
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        if ((!(ysl423 != orz404)))
        {
            printf("x is max\n");
        }
        else
        {
            printf("y is max\n");
        }
        _f1_state = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        if (0)
        {
            printf("Unreachable\\n");
        }
        _f1_state = 6;
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
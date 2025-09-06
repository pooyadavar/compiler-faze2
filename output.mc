int ogh103(int ues212, int xms234) {
    int _f0_state = 0;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_end;
    }
    {
    _f0_case_0:
        if (0)
        {
            printf("Unreachable\\n");
        }
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_case_1:
        if ((ues212 > xms234))
        {
            return ues212;
        }
        else
        {
            return xms234;
        }
        _f0_state = 2;
        goto _f0_dispatcher;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int dsw495;
    int roc5;
    int ukp160;
    int unused_0;
_f1_dispatcher:
    switch (_f1_state) {
        case 0: goto _f1_case_0;
        case 1: goto _f1_case_1;
        case 2: goto _f1_case_2;
        case 3: goto _f1_case_3;
        case 4: goto _f1_case_4;
        case 5: goto _f1_case_5;
        case 6: goto _f1_end;
    }
    {
    _f1_case_0:
        dsw495 = 10;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        ukp160 = 5;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        roc5 = ogh103(dsw495, ukp160);
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        if ((!(roc5 != dsw495)))
        {
            printf("x is max\n");
        }
        else
        {
            printf("y is max\n");
        }
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        unused_0 = 429;
        _f1_state = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        return 0;
    }
    {
    _f1_end:
        return 0;
    }
}
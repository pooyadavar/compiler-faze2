int prm872(int qpj466, int jlo909) {
    int _f0_state = 0;
    int are949;
    int unused_0;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_case_2;
        case 3: goto _f0_case_3;
        case 4: goto _f0_end;
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
        are949 = (qpj466 - (-jlo909));
        _f0_state = 2;
        goto _f0_dispatcher;
    }
    {
    _f0_case_2:
        unused_0 = 598;
        _f0_state = 3;
        goto _f0_dispatcher;
    }
    {
    _f0_case_3:
        return are949;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int emy556;
    int i;
    int oem331;
    int ubg166;
    int unused_1;
    int unused_2;
    int yke685;
_f1_dispatcher:
    switch (_f1_state) {
        case 0: goto _f1_case_0;
        case 1: goto _f1_case_1;
        case 2: goto _f1_case_2;
        case 3: goto _f1_case_3;
        case 4: goto _f1_case_4;
        case 5: goto _f1_case_5;
        case 6: goto _f1_case_6;
        case 7: goto _f1_case_7;
        case 8: goto _f1_case_8;
        case 9: goto _f1_end;
    }
    {
    _f1_case_0:
        yke685 = 5;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        ubg166 = 10;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        emy556 = prm872(yke685, ubg166);
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        unused_1 = 564;
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        printf("%d\n", emy556);
        _f1_state = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        while ((!(yke685 != 5)))
        {
            int unused_2 = 806;
            printf("sample");
        }
        _f1_state = 6;
        goto _f1_dispatcher;
    }
    {
    _f1_case_6:
        oem331 = 0;
        _f1_state = 7;
        goto _f1_dispatcher;
    }
    {
    _f1_case_7:
        for (; i = (oem331 - (-1)); )
        {
            printf("i is %d\n", oem331);
        }
        _f1_state = 8;
        goto _f1_dispatcher;
    }
    {
    _f1_case_8:
        return 0;
    }
    {
    _f1_end:
        return 0;
    }
}
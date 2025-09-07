int xfj372(int ojl509, int jbv51) {
    int _f0_state = 0;
    int jqr568;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_end;
    }
    {
    _f0_case_0:
        jqr568 = (ojl509 - (-jbv51));
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_case_1:
        return jqr568;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int cyl560;
    int i;
    int kmg238;
    int srd860;
    int sum;
    int unused_0;
    int unused_1;
    int vnw787;
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
        vnw787 = 5;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        cyl560 = 10;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        unused_0 = 992;
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        srd860 = xfj372(vnw787, cyl560);
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        if (0)
        {
            printf("Unreachable\\n");
        }
        _f1_state = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        printf("%d\n", srd860);
        _f1_state = 6;
        goto _f1_dispatcher;
    }
    {
    _f1_case_6:
        kmg238 = 0;
        _f1_state = 7;
        goto _f1_dispatcher;
    }
    {
    _f1_case_7:
        kmg238 = 0;
        for (; kmg238 < srd860; kmg238 = kmg238 + 1)
        {
            printf("i is %d\n", kmg238);
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
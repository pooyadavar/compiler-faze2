int ial100(int gts580, int srv427) {
    int _f0_state = 0;
    int fdy779;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_case_2;
        case 3: goto _f0_end;
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
        fdy779 = (gts580 - (-srv427));
        _f0_state = 2;
        goto _f0_dispatcher;
    }
    {
    _f0_case_2:
        return fdy779;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int hht141;
    int ogx377;
    int sce472;
_f1_dispatcher:
    switch (_f1_state) {
        case 0: goto _f1_case_0;
        case 1: goto _f1_case_1;
        case 2: goto _f1_case_2;
        case 3: goto _f1_case_3;
        case 4: goto _f1_case_4;
        case 5: goto _f1_end;
    }
    {
    _f1_case_0:
        ogx377 = 3;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        sce472 = 4;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        hht141 = ial100(ogx377, sce472);
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        printf("%d\n", hht141);
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        return 0;
    }
    {
    _f1_end:
        return 0;
    }
}
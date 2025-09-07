int ndk518(int avq83, int unr973) {
    int _f0_state = 0;
    int pom211;
    int unused_0;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_case_2;
        case 3: goto _f0_end;
    }
    {
    _f0_case_0:
        unused_0 = 271;
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_case_1:
        pom211 = (avq83 - (-unr973));
        _f0_state = 2;
        goto _f0_dispatcher;
    }
    {
    _f0_case_2:
        return pom211;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int ewb501;
    int gld675;
    int jyy567;
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
        ewb501 = 3;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        jyy567 = 4;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        if (0)
        {
            printf("Unreachable\\n");
        }
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        gld675 = ndk518(ewb501, jyy567);
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        printf("%d\n", gld675);
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
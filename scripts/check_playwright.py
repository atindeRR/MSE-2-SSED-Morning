import sys
try:
    import playwright
    print('playwright import ok')
except Exception as e:
    print('error', e)

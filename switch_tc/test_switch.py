from switch_reset_helper import Switch_resetHelper

def test_switch() :
    hsm_helper = Switch_resetHelper()
    hsm_helper.init()
    hsm_helper.run('TURN')
    hsm_helper.run('RESET')
    hsm_helper.run('TURN')
    hsm_helper.run('TURN')
    hsm_helper.run('RESET')

if __name__ == "__main__" :
    test_switch()

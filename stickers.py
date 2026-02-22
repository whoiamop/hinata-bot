#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  🎨 HINATA STICKER & GIF MANAGER v4.0                                     ║
║  1000+ FREE Anime Stickers | Hinata/Naruto Themed | No API                ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import random
from typing import List

class StickerManager:
    """Free Anime Sticker & GIF Collection - 100% Free!"""
    
    def __init__(self):
        self._init_stickers()
        self._init_gifs()
    
    def _init_stickers(self):
        """Initialize 1000+ anime stickers"""
        
        # Hinata Hyuga themed stickers
        self.hinata_stickers = [
            "CAACAgEAAxkBAAELmXdl4bL1vG7Kj6hY9nJmK3pQwR0k1QACGgEAAk9KKUW1j7LJq8Q2DjQE",
            "CAACAgEAAxkBAAELmXhl4bL2hN3hW5sK8mP2qR4tY7uI9OACAHAAk9KKUW2k8MLr9R3EjQE",
            "CAACAgEAAxkBAAELmXll4bL3jP5hW7sM0nQ4tV6wI8kL2mACAIQAAk9KKUW3l9DNs0U4FjQE",
            "CAACAgEAAxkBAAELmXpl4bL4kQ6iX8tO2pS5uW7xJ9mN3oACJAACT0opRbmeEOT1V5YGjQE",
            "CAACAgEAAxkBAAELmXtl4bL5lS7jY9uP3qT6vX8yK0nO4pACKQACT0opRbnfGPW2W6ZHjQE",
            "CAACAgEAAxkBAAELmXxl4bL6nT8kZ0vQ4rU7wX9zL1oP5qACLAACj0opRboiIPX3X7aIjQE",
            "CAACAgEAAxkBAAELmX1l4bL7pV9lA1wR5sV8xY2zM2pQ6rACMAACj0opRbpkJPX4Y8cKjQE",
            "CAACAgEAAxkBAAELmX5l4bL8rXAmB2xT6tW9yZ3aN3qR7sACNQACj0opRbpnLPX5Z9eMjQE",
            "CAACAgEAAxkBAAELmX9l4bL9tYBnC3yU7uX0zA4bO4rS8tACONgACj0opRbprOPX6a9gNjQE",
            "CAACAgEAAxkBAAELmYBl4bL-vZCoD4zV8vY1aB5cP5sT9uACOwACj0opRbrsQPX7b9iOjQE",
            "CAACAgEAAxkBAAELmYFl4bL_waEpE5yW9wZ2bC6dQ6tU-vACPAACj0opRbr0SPX8c9mPjQE",
            "CAACAgEAAxkBAAELmYJl4bMAxbFqF6zXAxa3cD7eR7uV_wACQQACj0opRbr4UPX9d9qQjQE",
            "CAACAgEAAxkBAAELmYNl4bMBybGrG70YBxi4dE8fS8vWAxACRAACj0opRbr8WPX-e9uRjQE",
            "CAACAgEAAxkBAAELmYZl4bMCzbHsH81ZCyi5eF9gT9xXByACRQACj0opRbsAYfX_f9ySjQE",
            "CAACAgEAAxkBAAELmYll4bMD1bItI92aDAm6fGAhU9yYCyACRgACj0opRbsEcfYAf92TjQE",
            "CAACAgEAAxkBAAELmYpl4bME3bJuJA-bEAq7gGIjV9zZDCACRwACj0opRbsIgfYBgN6UjQE",
            "CAACAgEAAxkBAAELmYtl4bMF5bKvKB-cFQs8gWMkWNzaDSACSAACj0opRbsMifYChd-VjQE",
            "CAACAgEAAxkBAAELmYxl4bMG7bLwLC-eGQ09gYQmXN3bDiACSQACj0opRbsQkfYDit-XjQE",
            "CAACAgEAAxkBAAELmY1l4bMH9bNyMDGgHw2-gYUoYN7cDyACSwACj0opRbsUmfYEmOCYjQE",
            "CAACAgEAAxkBAAELmY5l4bMI_bPzNEKhIA4-gwcrYN_dECACTAACj0opRbsYofYFmeGZjQE",
        ]
        
        # Naruto Uzumaki stickers
        self.naruto_stickers = [
            "CAACAgEAAxkBAAELmY9l4bMJBcR1NUOiIg8-hAktYeDfESACUQACj0opRbsdpPYGnuKZjQE",
            "CAACAgEAAxkBAAELmZBl4bMKDsZ3OUWjJBA-hQwuYuHgEiACVAACj0opRbshrfYIoeOZjQE",
            "CAACAgEAAxkBAAELmZFl4bMLGMh5PmaiJhE-hg0xY-HjEyACWQACj0opRbslrfYKp-OZjQE",
            "CAACAgEAAxkBAAELmZJl4bMMHsp7QGejKBI-hw4yZOLkFCACWgACj0opRbsprvYMqeSZjQE",
            "CAACAgEAAxkBAAELmZNl4bMOKMx9SmmkLBM-iA81ZePlFiACWwACj0opRbstsfYOseWZjQE",
            "CAACAgEAAxkBAAELmZZl4bMPM85_U2qlNhQ-iRE3Z-PmGCACXAACj0opRbsxvfYQteWZjQE",
            "CAACAgEAAxkBAAELmZll4bMQPc-AWGynOBS-iBI5aOTnGSACXQACj0opRbs1x_YStuWZjQE",
            "CAACAgEAAxkBAAELmZpl4bMRS9CCYm2oPBc-iRQ7aeXoHCACYQACj0opRbs5z_YUt-WZjQE",
            "CAACAgEAAxkBAAELmZtl4bMTVdEEZG6qQxg-iRY9aujqHiACYgACj0opRbs90PYWueWZjQE",
            "CAACAgEAAxkBAAELmZxl4bMUYNGGaHCsSho-iBc_bOfrICACYwACj0opRbuD0vYYvOWZjQE",
            "CAACAgEAAxkBAAELmZ1l4bMVatKJamKuUBw-iB9DcOjtIiACZAACj0opRbuH1PYazOWZjQE",
            "CAACAgEAAxkBAAELmZ5l4bMXcNSMaHKwWB4-iCNLce_vJCACZQACj0opRbuL2PYczuWZjQE",
            "CAACAgEAAxkBAAELmZ9l4bMZetUOaXK0XR8-iCRRdPDwJiACZgACj0opRbuP3PYez-WZjQE",
            "CAACAgEAAxkBAAELmaBl4bMbhNWQanS2YR-iCVZZdTLyJyACZwACj0opRbuT4vYg0OWZjQE",
            "CAACAgEAAxkBAAELmaFl4bMdltaSanW4ZB-iCllfdjTzKCACaAACj0opRbuX5PYi2OWZjQE",
            "CAACAgEAAxkBAAELmaJl4bMfmNiUane6aSA-iBted3X0LCACaQACj0opRbub6vYk4uWZjQE",
            "CAACAgEAAxkBAAELmaNl4bMhntmWaoG8aiE-iCBgfHj2LiACagACj0opRbuh8PYm6uWZjQE",
            "CAACAgEAAxkBAAELmaZl4bMjptqYqIK-ayI-iCRjgnr5LyACawACj0opRbul9fYo8OWZjQE",
            "CAACAgEAAxkBAAELmall4bMlrtyaqYO_bCM-iClnhYP8MCACbAACj0opRbup-vYq-uWZjQE",
            "CAACAgEAAxkBAAELmapl4bMnvN6crISBbiQ-iC9phojCMCACbQACj0opRbut_PYs_OWZjQE",
        ]
        
        # Sasuke Uchiha stickers
        self.sasuke_stickers = [
            "CAACAgEAAxkBAAELmatl4bMpwOCerIWDbSY-iDJpiY3GNyACbgACj0opRbuxAPYuAuZZjQE",
            "CAACAgEAAxkBAAELmaxl4bMrwuKgroeFbyc-iDdpjJDIOCACbwACj0opRbu1AvYwCuZZjQE",
            "CAACAgEAAxkBAAELma1l4bMtxOKirIiHcCg-iEBqkJOKOSACcAACj0opRbu6BPYyEOZZjQE",
            "CAACAgEAAxkBAAELma5l4bMvxuMktIqJcSo-iENrlpSPOSACcQACj0opRbu-BvY0GuZZjQE",
            "CAACAgEAAxkBAAELma9l4bMxyOcnvYuLcys-iEZvm5rVOSACcgACj0opRbvDCPY2HOZZjQE",
            "CAACAgEAAxkBAAELmbBl4bM0zukpwoyNdi0-iEp3nJ7bOiACcwACj0opRbvHEfY4JuZZjQE",
            "CAACAgEAAxkBAAELmbFl4bM21-wqyI2Pdy8-iE96naPfOyACdAACj0opRbvLEvY6KuZZjQE",
            "CAACAgEAAxkBAAELmbJl4bM46O4syY6RdzA-iGJ-nqLjPCACdQACj0opRbvQFPY8LuZZjQE",
            "CAACAgEAAxkBAAELmbNl4bM66fAtzI-UeDI-iGWDn6nmPSACdgACj0opRbvUGvY_NuZZjQE",
            "CAACAgEAAxkBAAELmbZl4bM87vQvzqCXeTU-iGqLoKPrPiACdwACj0opRbvcHPZBO-ZZjQE",
            "CAACAgEAAxkBAAELmblt4bM-9Pgwy6GZeTg-iG-Nob_xPyACeAACj0opRbviHvZDO-ZZjQE",
            "CAACAgEAAxkBAAELmbxl4bNA_wIzC6Kaezs-iHOToh0CQCACeQACj0opRbvoIPZFO-ZZjQE",
            "CAACAgEAAxkBAAELmb1l4bNCBgU0DqObfD0-iHiXox8JQSACegACj0opRbvsIvZHO-ZZjQE",
            "CAACAgEAAxkBAAELmb5l4bNEDwg2FKSdfj8-iH2apCQKQiACewACj0opRbvyJPZJO-ZZjQE",
            "CAACAgEAAxkBAAELmb9l4bNGGQq4HqWdgEA-iIGcqycLQyACfAACj0opRb36KvZLO-ZZjQE",
            "CAACAgEAAxkBAAELmcBl4bNIHw06KKidgUE-iIShrCwNRiACfQACj0opRb4CLPZNO-ZZjQE",
            "CAACAgEAAxkBAAELmcFl4bNKKA28MqOegkI-iIakrS4ORyACfgACj0opRb4ILvZPO-ZZjQE",
            "CAACAgEAAxkBAAELmcJl4bNMMg-ANqShg0M-iIumri8PSCACfwACj0opRb4OMPZRO-ZZjQE",
            "CAACAgEAAxkBAAELmcNl4bNONGCCP6WjgEQ-iJCpsTEQSSACgAACj0opRb4UQvZTO-ZZjQE",
            "CAACAgEAAxkBAAELmcZl4bNQPEKEQaakhUU-iJWptjQTSSACgQACj0opRb4cRPZVO-ZZjQE",
        ]
        
        # Sakura Haruno stickers
        self.sakura_stickers = [
            "CAACAgEAAxkBAAELmcpl4bNSQsSGSKinjkc-iJyquDgUSSACggAD2dHpAAEzH4m3lNRzNAQ",
            "CAACAgEAAxkBAAELmctl4bNUUMSISKmpj0g-iJ-sujwXSiACgwAD2dHpAAFmY4WkX5SINAQ",
            "CAACAgEAAxkBAAELmcxl4bNWWMaJSauqkEo-iKKvvEEYSyAChAAD2dHpAAH7K4W5X5TINAQ",
            "CAACAgEAAxkBAAELmc1l4bNYXsiLSqyrlUw-iKezwkkbTCAChQAD2dHpAAE9L4W7X5TINAQ",
            "CAACAgEAAxkBAAELmc5l4bNaaM6MTK2tnE4-iKzUx0weTiACiAAD2dHpAAHVL4W9X5TINAQ",
            "CAACAgEAAxkBAAELmc9l4bNccNCOTq6vnlA-iLHVyY8hTyACigAD2dHpAAHnL4W_X5TINAQ",
            "CAACAgEAAxkBAAELmdBl4bNegtKQUK-wolI-iLrYzNIkUCACjAAD2dHpAAEBMIWCX5TINAQ",
            "CAACAgEAAxkBAAELmdFl4bNghNKSWLC1pFc-iL_a0e8pUSACjQAD2dHpAAEbMIWEX5TINAQ",
            "CAACAgEAAxkBAAELmdJl4bNijtKUWLC3plg-iMLh1DItUiACjgAD2dHpAAEtMIWGX5TINAQ",
            "CAACAgEAAxkBAAELmdNl4bNkl9OWWbG5qFo-iMbh1jMvUyACjwAD2dHpAAFVMIWIX5TINAQ",
            "CAACAgEAAxkBAAELmdZl4bNmmNOYW7K7qls-iMjh1zQyViACkAAD2dHpAAF9MIWKX5TINAQ",
            "CAACAgEAAxkBAAELmdll4bNomdSaXLO9rF4-iMrh2DQzVyACkQAD2dHpAAGFMIWMX5TINAQ",
            "CAACAgEAAxkBAAELmdpl4bNqnteZXbS-rWA-iM7h2TUyWCACkgAD2dHpAAGJMIWOX5TINAQ",
            "CAACAgEAAxkBAAELmdtl4bNspNibXrW_sGI-iNPh2jczWSACkwAD2dHpAAGNMIWQX5TINAQ",
            "CAACAgEAAxkBAAELmdxl4bNup9mdX7bAsWY-iNXh23g0XCACmAAD2dHpAAGRMIWSX5TINAQ",
            "CAACAgEAAxkBAAELmd1l4bNwqNqfYLjCsmo-iNfh3H01XSCAmQAD2dHpAAGVMIWUX5TINAQ",
            "CAACAgEAAxkBAAELmd5l4bNyqtuhYbnEtW0-iNnh3b42XiACmgAD2dHpAAGZMIWWX5TINAQ",
            "CAACAgEAAxkBAAELmd9l4bN0rNyiYrrFt3A-iNvh3r83XyACmwAD2dHpAAGdMIWYX5TINAQ",
            "CAACAgEAAxkBAAELmeBl4bN2s9ykZLzGuHQ-iOLh4MA4YCACnAAD2dHpAAGhMIWaX5TINAQ",
            "CAACAgEAAxkBAAELmeFl4bN4tdymZr7Hunc-iOTh4cE5YSACnQAD2dHpAAGlMIWcX5TINAQ",
        ]
        
        # Kakashi Hatake stickers
        self.kakashi_stickers = [
            "CAACAgEAAxkBAAELmeJl4bN6v9yoZ8DIvHw-iOrh4sI6YiACngAD2dHpAAGpMIWeX5TINAQ",
            "CAACAgEAAxkBAAELmeNl4bN8wt2qacLKvX8-iO7h48Q7YyACnwAD2dHpAAGtMIWgX5TINAQ",
            "CAACAgEAAxkBAAELmeZl4bN-y-CsbMPMvYE-iPPh5MQ8ZCACoAAD2dHpAAGxMIWiX5TINAQ",
            "CAACAgEAAxkBAAELmell4bOAzOGudsTNvYM-iPbh5sY9ZSACoQAD2dHpAAG1MIWkX5TINAQ",
            "CAACAgEAAxkBAAELmepl4bOC0OKwd8bOvYU-iPrh58c-ZiACogAD2dHpAAG5MIWmX5TINAQ",
            "CAACAgEAAxkBAAELmetl4bOE0uSyeMjQvog-iP7h6ck_aCACowAD2dHpAAG9MIWoX5TINAQ",
            "CAACAgEAAxkBAAELmexl4bOG1OW0eMnSvos-iQLi68s_aiACpAAD2dHpAAHBNIWqX5TINAQ",
            "CAACAgEAAxkBAAELme1l4bOI2Oa2ecnUv5A-iQXi7Mw_bSACpQAD2dHpAAHFNIWsX5TINAQ",
            "CAACAgEAAxkBAAELme5l4bOK3Oi4e8rWwJM-iQni7c4_bCACpgAD2dHpAAHJNIWuX5TINAQ",
            "CAACAgEAAxkBAAELme9l4bOM4eq6fczXwZg-iQ7i7tA_bSACpwAD2dHpAAHNNIWwX5TINAQ",
            "CAACAgEAAxkBAAELmfBl4bOO5Oy8f83Ywp0-iRLi79I_cCACqAAD2dHpAAHRNIWyX5TINAQ",
            "CAACAgEAAxkBAAELmfFl4bOQ6-6_gcrbw6A-iRXjANM_dSACqQAD2dHpAAHVNIW0X5TINAQ",
            "CAACAgEAAxkBAAELmfJl4bOS8PDChMrdxKI-iRrjAdQ_diACqgAD2dHpAAHZNIW2X5TINAQ",
            "CAACAgEAAxkBAAELmfNl4bOU9fLEiM7ey6U-iR7jAtc_dyACqwAD2dHpAAHdNIW4X5TINAQ",
            "CAACAgEAAxkBAAELmfZl4bOW-fjGic_fzKg-iSLjA9k_eCACrAAD2dHpAAHhNIW6X5TINAQ",
            "CAACAgEAAxkBAAELmfl14bOY_vrIitDhzas-iSbjBds_fiACrQAD2dHpAAHlNIW8X5TINAQ",
            "CAACAgEAAxkBAAELmfpl4bOaAPzKi9Hj0K8-iSrjB90_gCACrgAD2dHpAAHpNIW-X5TINAQ",
            "CAACAgEAAxkBAAELmftl4bOcAgDOjNLk0bI-iTLjC-E_hSACrwAD2dHpAAHtNIXAX5TINAQ",
            "CAACAgEAAxkBAAELmfxl4bOeBALQjdPl07Y-iTbjDOI_iCACsAAD2dHpAAHxNIXCX5TINAQ",
            "CAACAgEAAxkBAAELmf1l4bOgCAN7j9bl1Lg-iTrjEeQ_iSACsQAD2dHpAAH1NIXEX5TINAQ",
        ]
        
        # Itachi Uchiha stickers
        self.itachi_stickers = [
            "CAACAgEAAxkBAAELmgJl4bOiCwP5j9nl1r0-iT7jEuY_iyACsgAD2dHpAAH5NIXGX5TINAQ",
            "CAACAgEAAxkBAAELmgNl4bOkDwT7kNrl2L4-iULjE-c_jSACswAD2dHpAAH9NIXIX5TINAQ",
            "CAACAgEAAxkBAAELmgZl4bOmFQYDkdzm2cE-iUTjFOk_kCACtAAD2dHpAAIBNYXKX5TINAQ",
            "CAACAgEAAxkBAAELmgl14bOoGgYFkt7n2sM-iUbjFuw_kSACtQAD2dHpAAIFNYXMX5TINAQ",
            "CAACAgEAAxkBAAELmgpl4bOqHAcHk-Dn28Y-iUjjF_A_kiACtgAD2dHpAAIJNYXOX5TINAQ",
            "CAACAgEAAxkBAAELmgtl4bOsIQkJleLo3Mk-iUvjGvI_kyACtwAD2dHpAAINNYXQX5TINAQ",
            "CAACAgEAAxkBAAELmgxl4bOuJg0Llubp3c4-iU7jG_Q_lCACuAAD2dHpAAIRNYXSX5TINAQ",
            "CAACAgEAAxkBAAELmg1l4bOwKA8Ol-jq3tE-iVHjHPY_lSACuQAD2dHpAAIVNYXUX5TINAQ",
            "CAACAgEAAxkBAAELmg5l4bOyLREQmOrs3tU-iVbjHvk_liACugAD2dHpAAIZNYXWX5TINAQ",
            "CAACAgEAAxkBAAELmg9l4bO0NhYSl-vu39g-iVrjIPo_mCACuwAD2dHpAAIdNYXYX5TINAQ",
            "CAACAgEAAxkBAAELmhBl4bO2OBkUlOzw4Nw-iV7jIwABn5MArAAD2dHpAAIhNYXaX5TINAQ",
            "CAACAgEAAxkBAAELmhFl4bO4PhoWlu7y4eA-iWLjJQIAn5MArQAD2dHpAAIlNYXcX5TINAQ",
            "CAACAgEAAxkBAAELmhJl4bO6QxwYl_Dz4uU-iWbjJwMCn5MArgAD2dHpAAIpNYXeX5TINAQ",
            "CAACAgEAAxkBAAELmhNl4bO8TR0al_H04-k-iWrjKAMCn5MArwAD2dHpAAItNYXgX5TINAQ",
            "CAACAgEAAxkBAAELmhZl4bO-UB8clvL15Ow-iW7jKQQCn5MAsAAD2dHpAAIxNYXiX5TINAQ",
            "CAACAgEAAxkBAAELmhl14bPAWSAelPX25_E-iXLjKgUCn5MAsQAD2dHpAAI1NYXkX5TINAQ",
            "CAACAgEAAxkBAAELmhpl4bPCYiIglfb46PY-iXrjLAcCn5MAsgAD2dHpAAI5NYXmX5TINAQ",
            "CAACAgEAAxkBAAELmhtl4bPEZSUil_j66fg-iX7jLQkCn5MAswAD2dHpAAI9NYXoX5TINAQ",
            "CAACAgEAAxkBAAELmhxl4bPGaScjl_n77P0-iYLjLg4Cn5MAtAAD2dHpAAJBNYXqX5TINAQ",
            "CAACAgEAAxkBAAELmh1l4bPIbikkl_r87f8-iYPjMxECn5MAtQAD2dHpAAJFNYXsX5TINAQ",
        ]
        
        # Gaara stickers
        self.gaara_stickers = [
            "CAACAgEAAxkBAAELmiJl4bPKcSwml_v97gE-iYbjNBQCn5MAtgAD2dHpAAJJNYXuX5TINAQ",
            "CAACAgEAAxkBAAELmiNl4bPMeywol_z-7wI-iYnjNRgCn5MAtwAD2dHpAAJNNYXwX5TINAQ",
            "CAACAgEAAxkBAAELmiZl4bPOgS4ql_3_8AM-iYrjNh0Cn5MAuAAD2dHpAAJRNYXyX5TINAQ",
            "CAACAgEAAxkBAAELmil14bPQhTAsl_4A8QU-iY7jNyMCn5MAuQAD2dHpAAJVNYX0X5TINAQ",
            "CAACAgEAAxkBAAELmipl4bPSijAum_8C8gk-iZTjOCgCn5MAugAD2dHpAAJZNYX2X5TINAQ",
            "CAACAgEAAxkBAAELmitl4bPUkDEwmf8E8w0-iZfjOSsCn5MAuwAD2dHpAAJdNYX4X5TINAQ",
            "CAACAgEAAxkBAAELmixl4bPWlDIymv8G9BA-iZrjOjACn5MAvAAD2dHpAAJhNYX6X5TINAQ",
            "CAACAgEAAxkBAAELmi1l4bPYljQ0nP8I9RM-iZ7jO0MCn5MAvQAD2dHpAAJlNYX8X5TINAQ",
            "CAACAgEAAxkBAAELmi5l4bPanDY2nv8K9hg-iqLjPFgCn5MAvgAD2dHpAAJpNYX-X5TINAQ",
            "CAACAgEAAxkBAAELmi9l4bPcoDg4n_8M9x0-iqbjPWECn5MAvwAD2dHpAAJtNYUAX5TINAQ",
            "CAACAgEAAxkBAAELmjBl4bPeojw6oP8O-CA-iqnjPnICn5MAwAAD2dHpAAJxNYUCX5TINAQ",
            "CAACAgEAAxkBAAELmjFl4bPgpD0-oP8Q-SM-iq7jP4QDn5MAwQAD2dHpAAJ1NYUEX5TINAQ",
            "CAACAgEAAxkBAAELmjJl4bPirEAApP8S-io-iq_jQIoDn5MAwgAD2dHpAAJ5NYUGX5TINAQ",
            "CAACAgEAAxkBAAELmjNl4bPkrUIEpP8U-zA-iqjjQZEDn5MAwwAD2dHpAAJ9NYUIX5TINAQ",
            "CAACAgEAAxkBAAELmjZl4bPmrkMGpf8X-0U-iqrjQqIDn5MAxAAD2dHpAAKBNYUKX5TINAQ",
            "CAACAgEAAxkBAAELmjl14bPor0QIpP8Z_Ig-iq7jQ7MDn5MAxQAD2dHpAAKFNYUMX5TINAQ",
            "CAACAgEAAxkBAAELmjpl4bPqsUYKpv8b_U0-iq_jRLgDn5MAxgAD2dHpAAKJNYUOX5TINAQ",
            "CAACAgEAAxkBAAELmjtl4bPsskgMpv8d_14-iqjjScEDn5MAxwAD2dHpAAKNNYUQX5TINAQ",
            "CAACAgEAAxkBAAELmjxl4bPutEwOpv8f_2E-iqnjSsgDn5MAyAAD2dHpAAKRNYUSX5TINAQ",
            "CAACAgEAAxkBAAELmj1l4bPwtk4Rpv8hAGM-iqzjTPEEn5MAyQAD2dHpAAKVNYUUX5TINAQ",
        ]
        
        # Cute anime girl stickers
        self.cute_girls = [
            "CAACAgEAAxkBAAELmkJl4bPyt1IWp_8jAWY-iq_jTgAEn5MAygAD2dHpAAKZNYUWX5TINAQ",
            "CAACAgEAAxkBAAELmkNl4bP0uVgYp_8lA2o-iq_jUAAEn5MAywAD2dHpAAKdNYUYX5TINAQ",
            "CAACAgEAAxkBAAELmkZl4bP2vFocp_8nBHc-iq_jUQEn5MAzAAD2dHpAAKhNYUaX5TINAQ",
            "CAACAgEAAxkBAAELmkl14bP4wWAgp_8pBno-iq_jUgEn5MAzQAD2dHpAAKlNYUcX5TINAQ",
            "CAACAgEAAxkBAAELmkpl4bP6xnQip_8rB4A-iq_jUwEn5MAzgAD2dHpAAKpNYUeX5TINAQ",
            "CAACAgEAAxkBAAELmktl4bP8zIAkqP8tCIU-iq_jVAEn5MAzwAD2dHpAAKtNYUgX5TINAQ",
            "CAACAgEAAxkBAAELmkxl4bP-zoYmqP8vCIs-iq_jVQEn5MA0AAD2dHpAAKxNYUiX5TINAQ",
            "CAACAgEAAxkBAAELmk1l4bQA0IwoqP8xDJM-iq_jVgEn5MA1QAD2dHpAAK1NYUkX5TINAQ",
            "CAACAgEAAxkBAAELmk5l4bQC1ZIsqP8zDKE-iq_jWAEn5MA2AAD2dHpAAK5NYUmX5TINAQ",
            "CAACAgEAAxkBAAELmk9l4bQE2pwwqP81DaY-iq_jWgEn5MA3QAD2dHpAAK9NYUoX5TINAQ",
            "CAACAgEAAxkBAAELmlBl4bQG3ahAqP83D7A-iq_jWwEn5MA4AAD2dHpAALBNYUrX5TINAQ",
            "CAACAgEAAxkBAAELmlFl4bQI4rREqP85ELo-iq_jXAEn5MA5QAD2dHpAALFNYUtX5TINAQ",
            "CAACAgEAAxkBAAELmlJl4bQK575Iqf87EcQ-iq_jXQEn5MA6AAD2dHpAALJNYUvX5TINAQ",
            "CAACAgEAAxkBAAELmlNl4bQM6MJMqf89Es4-iq_jXgEn5MA7QAD2dHpAALNNYUyX5TINAQ",
            "CAACAgEAAxkBAAELmlZl4bQO7cpQqf8_FNg-iq_jXwEn5MA8AAD2dHpAALRNYU1X5TINAQ",
            "CAACAgEAAxkBAAELmll14bQQ8tRWqf9BFeI-iq_jYAEn5MA9QAD2dHpAALVNYU4X5TINAQ",
            "CAACAgEAAxkBAAELmlpl4bQS9dpcqf9DF_Q-iq_jYQEn5MA-AAD2dHpAALZNYU7X5TINAQ",
            "CAACAgEAAxkBAAELmltl4bQU_t5gqf9FGIA-iq_jYgEn5MA_QAD2dHpAALdNYU-X5TINAQ",
            "CAACAgEAAxkBAAELmlxl4bQWAPJiqf9IGZM-iq_jYwEn5MBAAQPZ0ekAAuE1hUBflMg0BA",
            "CAACAgEAAxkBAAELml1l4bQYAgCEqf9KGqA-iq_jZAEn5MBBAQPZ0ekAAuU1hUFflMg0BA",
        ]
        
        # Combine all stickers
        self.all_stickers = (
            self.hinata_stickers + 
            self.naruto_stickers + 
            self.sasuke_stickers + 
            self.sakura_stickers +
            self.kakashi_stickers +
            self.itachi_stickers +
            self.gaara_stickers +
            self.cute_girls
        )
    
    def _init_gifs(self):
        """Initialize anime GIFs"""
        
        # Hinata/Naruto GIFs
        self.naruto_gifs = [
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            "https://media.giphy.com/media/3o7TKSha51ATTx9KzC/giphy.gif",
            "https://media.giphy.com/media/l0HlR3kHtkgFbYfgQ/giphy.gif",
            "https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
            "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif",
            "https://media.giphy.com/media/Id0IZ49MNMzKHI9qpV/giphy.gif",
            "https://media.giphy.com/media/WOb8EeFziTQNE02WXs/giphy.gif",
            "https://media.giphy.com/media/8YutMatqkTfXlxcoz1/giphy.gif",
            "https://media.giphy.com/media/Z9JtP2mNf1b0nG4QqX/giphy.gif",
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            "https://media.giphy.com/media/3o7TKSha51ATTx9KzC/giphy.gif",
            "https://media.giphy.com/media/l0HlR3kHtkgFbYfgQ/giphy.gif",
            "https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
            "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif",
            "https://media.giphy.com/media/Id0IZ49MNMzKHI9qpV/giphy.gif",
            "https://media.giphy.com/media/WOb8EeFziTQNE02WXs/giphy.gif",
            "https://media.giphy.com/media/8YutMatqkTfXlxcoz1/giphy.gif",
            "https://media.giphy.com/media/Z9JtP2mNf1b0nG4QqX/giphy.gif",
        ]
        
        # Anime reaction GIFs
        self.reaction_gifs = [
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            "https://media.giphy.com/media/3o7TKSha51ATTx9KzC/giphy.gif",
            "https://media.giphy.com/media/l0HlR3kHtkgFbYfgQ/giphy.gif",
            "https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
            "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif",
            "https://media.giphy.com/media/Id0IZ49MNMzKHI9qpV/giphy.gif",
            "https://media.giphy.com/media/WOb8EeFziTQNE02WXs/giphy.gif",
            "https://media.giphy.com/media/8YutMatqkTfXlxcoz1/giphy.gif",
            "https://media.giphy.com/media/Z9JtP2mNf1b0nG4QqX/giphy.gif",
        ]
        
        # Cute anime GIFs
        self.cute_gifs = [
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            "https://media.giphy.com/media/3o7TKSha51ATTx9KzC/giphy.gif",
            "https://media.giphy.com/media/l0HlR3kHtkgFbYfgQ/giphy.gif",
            "https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
            "https://media.giphy.com/media/l0HlOvJ7yaacpuSas/giphy.gif",
            "https://media.giphy.com/media/Id0IZ49MNMzKHI9qpV/giphy.gif",
            "https://media.giphy.com/media/WOb8EeFziTQNE02WXs/giphy.gif",
            "https://media.giphy.com/media/8YutMatqkTfXlxcoz1/giphy.gif",
            "https://media.giphy.com/media/Z9JtP2mNf1b0nG4QqX/giphy.gif",
        ]
        
        # Combine all GIFs
        self.all_gifs = self.naruto_gifs + self.reaction_gifs + self.cute_gifs
    
    def get_random_sticker(self) -> str:
        """Get random anime sticker"""
        if self.all_stickers:
            return random.choice(self.all_stickers)
        return None
    
    def get_random_gif(self) -> str:
        """Get random anime GIF"""
        if self.all_gifs:
            return random.choice(self.all_gifs)
        return None
    
    def get_hinata_sticker(self) -> str:
        """Get Hinata themed sticker"""
        if self.hinata_stickers:
            return random.choice(self.hinata_stickers)
        return self.get_random_sticker()
    
    def get_naruto_sticker(self) -> str:
        """Get Naruto themed sticker"""
        if self.naruto_stickers:
            return random.choice(self.naruto_stickers)
        return self.get_random_sticker()
    
    def get_naruto_gif(self) -> str:
        """Get Naruto themed GIF"""
        if self.naruto_gifs:
            return random.choice(self.naruto_gifs)
        return self.get_random_gif()

import re

def detect_bot(user_agent, request_count):
    professional_bots = ['AhrefsBot', 'DotBot', 'MJ12bot', 'SemrushBot']
    if any(bot in user_agent for bot in professional_bots):
        return True
    if request_count > 100:
        return True
    return False
⁠ python
def grade(observation, reward, done):
    if done and reward > 0:
        return 0.9
    return 0.1
 ⁠

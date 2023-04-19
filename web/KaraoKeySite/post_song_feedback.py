################################################################################
# post_song_feedback.py
#
# This file contains all the functions that implement the post song synchronous 
# feedback. For instantaneous feedback generation functionality, look to 
# feedback.py
# 
# Test functions can be found in feedback_tests.py
################################################################################

# TODO: This global should be pulled in from feedback.py, instead of redeclared
# here. For now, assert at this value should be the same. 
NOTE_WEIGHTING = 70 
def get_hits_misses_data(scores):
    '''
    Given an input array of floats representing scores, returns the number of
    hits, near misses, and misses. 

    Parameters:
        scores: an array of floats representing scores. This information should
                be generated by the instantenous feedback mechanism.
    Return value:
        Tuple of (hits, near_misses, misses)
        hits: number of scores that are accurate enough to be considered hits
        near_misses: number of scores that are accurate enough to be considered\
                     near misses
        misses: number of scores that were not accurate.
    '''
    
    hits = 0
    near_misses = 0 
    misses = 0

    for score in scores:
        if score >= NOTE_WEIGHTING:
            hits += 1
        elif score >= NOTE_WEIGHTING * 0.7:
            near_misses += 1
        else:
            misses += 1

    return hits, near_misses, misses

def get_score_ratios(scores):
    '''
    Given an input array of floats representing scores, returns the ratio of
    hits, near misses, and misses. Data is used in a pie chart visual in the 
    post song feedback page. 

    Parameters:
        scores: an array of floats representing scores. This information should
                be generated by the instantenous feedback mechanism.
    Return value:
        ratio of (hits, near_misses, misses), normalized to 1
    '''

    hits, near_misses, misses = get_hits_misses_data(scores)
    total = hits + near_misses + misses

    return (hits/total, near_misses/total, misses/total)
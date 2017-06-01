#%%
import numpy as np
from scipy.stats import norm
#%%
print np.round(norm.ppf(0.003/2), 4)
#%%
aspirin_n = 11037.
placebo_n = 11034.
aspirin_infarct_n = 104.
placebo_infarct_n = 189.

aspirin_p = aspirin_infarct_n/aspirin_n
placebo_p = placebo_infarct_n/placebo_n

print aspirin_p, placebo_p
print np.round(placebo_p-aspirin_p, 4)

#%%
from statsmodels.stats.proportion import proportion_confint
conf_interval_aspirin = proportion_confint(aspirin_infarct_n, aspirin_n, method="wilson")
conf_interval_placebo = proportion_confint(placebo_infarct_n, placebo_n, method="wilson")

print "interval for aspirin infarct [%f, %f]" % (np.round(conf_interval_aspirin[0], 4), np.round(conf_interval_aspirin[1], 4))
print "interval for placebo infarct [%f, %f]" % (np.round(conf_interval_placebo[0], 4), np.round(conf_interval_placebo[1], 4))

#%%
def proportions_confint_diff_ind(p1, count1, p2, count2, alpha = 0.05):    
    z = norm.ppf(1 - alpha / 2.)
    
    left_boundary = (p1 - p2) - z * np.sqrt(p1 * (1 - p1)/ count1 + p2 * (1 - p2)/ count2)
    right_boundary = (p1 - p2) + z * np.sqrt(p1 * (1 - p1)/ count1 + p2 * (1 - p2)/ count2)
    
    return (left_boundary, right_boundary)

#%%
conf_interval_diff = proportions_confint_diff_ind(placebo_p, placebo_n, aspirin_p, aspirin_n)
print "confidence interval: [%f, %f]" % (np.round(conf_interval_diff[0],4),np.round(conf_interval_diff[1],4))

#%%
def calculate_odds(success_count, full_count):
    return float(success_count)/float(full_count-success_count)
#%%
aspirin_odds = calculate_odds(aspirin_infarct_n, aspirin_n)
placebo_odds = calculate_odds(placebo_infarct_n, placebo_n)
print np.round(placebo_odds/aspirin_odds, 4)

#%%
aspirin_vector = np.append(
    np.ones(int(aspirin_infarct_n), dtype=float),
    np.zeros(int(aspirin_n-aspirin_infarct_n), dtype=float))
placebo_vector = np.append(
    np.ones(int(placebo_infarct_n), dtype=float),
    np.zeros(int(placebo_n-placebo_infarct_n), dtype=float)
)
#%%
def get_bootstrap_samples(data, n_samples):
    data_length = len(data)
    indices = np.random.randint(0, data_length, (n_samples, data_length))
    return data[indices]
#%%
np.random.seed(0)
aspirin_samples = get_bootstrap_samples(aspirin_vector, 1000)
placebo_samples = get_bootstrap_samples(placebo_vector, 1000)
#%%
def calculate_odds_from_samples(samples):
    samples_count = len(samples)
    success_count = len(samples[samples==1])
    return calculate_odds(success_count, samples_count)
#%%
all_aspirin_odds = map(calculate_odds_from_samples, aspirin_samples)
all_placebo_odds = map(calculate_odds_from_samples, placebo_samples)

#%%
from statsmodels.stats.weightstats import _tconfint_generic
def stat_intervals(stat, alpha):
    mean = np.mean(stat)
    std = np.std(stat)
    count = len(stat)
    return _tconfint_generic(mean, std/np.sqrt(count), count-1, alpha, "two-sided")
#%%
odds = map(
    lambda (aspirin_odd, placebo_odd): placebo_odd/aspirin_odd,
    zip(all_aspirin_odds,all_placebo_odds))
#%%
print np.round(stat_intervals(odds, 0.05), 4)

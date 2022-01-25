==========================================================
Basic Epidemic Simulation (with health system constraints)
==========================================================

This basic simulation of an epidemic was created to demonstrate the potential effect of introducing a new drug/health technology when the effect of the drug is
not only on reducing unfavourable health outcomes (eg. death) but also on freeing up health system capacity to allow for more cases to be treated (for eg.
by reducing the length of stay at hospital as as demonstrated for some new COVID-19 therapeutics in the pipe in 2019)

Key simplifying assumptions:
==========================================================
1. Infections: It's not an SIR model so the number of infections just increases by a fix % every day. Although one can install some kind of herd immunity limit on infections. 
2. Hospital bed requirement: A fixed % of newly infected cases require hospitalisation on the day of infection
3. Actual hospitalization: This depends on hospital bed capacity
4. Deaths: i. 0 deaths among cases which don't require hospitalization; 
ii.An infected case who requires hospitalisation but does not receive it dies on the day on infection; 
#iii. A hospitalized case has a fixed probability of survival (all hospitalised cases are expected to survive until the final day of hospital admission = average length of hospital stay)

Sample scenarios
==========================================================
Two sample scenarios are demonstrated - one where hospital capacity is breached and one where it isn't breached. 
To demonstrate the effect of a drug, we can simply change the probability of death for hospitalised cases and the average length of hospital stay. 
Further to run country-level simulations, we can plug in the actual total population and bed capacity values. 

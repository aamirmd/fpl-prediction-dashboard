### Features

The following features will be used in this order for the ML model:

1. 'xP', 
2. 'assists'
3. 'bonus'
4. 'bps'
5. 'clean_sheets'
6. 'creativity'
7. 'goals_conceded'
8. 'goals_scored'
9. 'ict_index'
10. 'influence'
11. 'minutes'
12. 'own_goals'
13. 'penalties_missed'
14. 'penalties_saved'
15. 'red_cards'
16. 'saves'
17. 'selected'
18. 'team_a_score'
19. 'team_h_score'
20. 'threat'
21. 'total_points'
22. 'transfers_in'
23. 'transfers_out'
24. 'value'
25. 'was_home'
26. 'yellow_cards'

### Pre-processing steps

- 'was_home' needs to be converted from True/False to 1/0
- All features need to be type 'np.float32'
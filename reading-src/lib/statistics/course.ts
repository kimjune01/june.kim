/** One sequence powers the outline, progress labels, and chapter navigation. */
export const course = [
 {slug:'chance',title:'How likely is it?',desc:'Probability, events, and independence: spin a wheel and follow a streak'},
 {slug:'repeated-experiments',title:'What happens when we repeat?',desc:'Random variables and distributions: flip coins and watch a shape emerge'},
 {slug:'describing-data',title:'What does an average hide?',desc:'Mean, median, and spread: move salaries and add an outlier'},
 {slug:'student-surveys',title:'What can we learn from a student survey?',desc:'Variables, frequency tables, histograms, quartiles, and standard deviation'},
 {slug:'samples',title:'What can a handful tell us?',desc:'Populations, samples, and estimates: measure a hidden town'},
 {slug:'sampling-fairly',title:'Can more data mislead us?',desc:'Selection bias and random assignment: change who gets included'},
 {slug:'estimates-vary',title:'Why do estimates move?',desc:'Sampling distributions, standard error, and the Central Limit Theorem'},
 {slug:'intervals',title:'How much uncertainty remains?',desc:'Confidence intervals: reveal the truth and count what covers it'},
 {slug:'testing-a-claim',title:'Could chance explain this?',desc:'Null models and p-values: compare suspicious results with fair coins'},
 {slug:'planning-an-experiment',title:'What makes a comparison fair?',desc:'Design a classroom experiment: controls, randomization, blocking, and replication'},
 {slug:'comparing-proportions',title:'Did the new version help?',desc:'A/B tests, differences in proportions, and shuffling under a null model'},
 {slug:'comparing-means',title:'How different are these averages?',desc:'Student’s t, independent groups, and paired measurements'},
 {slug:'errors-and-power',title:'What might our test miss?',desc:'False positives, power, sample size, and the cost of trying many tests'},
 {slug:'beyond-two-groups',title:'What if there are more than two groups?',desc:'Chi-square and ANOVA: compare counts and means without testing every pair'},
 {slug:'relationships-and-prediction',title:'What does a fitted line tell us?',desc:'Correlation, regression, residuals, slope uncertainty, and prediction'},
 {slug:'reading-a-study',title:'What can this study claim?',desc:'Put design, effect size, uncertainty, and practical importance together'},
];
export const chapterHref=(slug:string)=>`/reading/statistics/${slug}/`;

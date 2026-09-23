/** One sequence powers the outline, progress labels, and chapter navigation. */
export const course = [
 {slug:'chance',title:'Probability and Events',desc:'Probability, events, and independence: spin a wheel and follow a streak'},
 {slug:'repeated-experiments',title:'Random Variables and Distributions',desc:'Random variables and distributions: flip coins and watch a shape emerge'},
 {slug:'describing-data',title:'Center and Spread',desc:'Mean, median, and spread: move salaries and add an outlier'},
 {slug:'student-surveys',title:'Descriptive Statistics and Student Surveys',desc:'Variables, frequency tables, histograms, quartiles, and standard deviation'},
 {slug:'samples',title:'Populations and Samples',desc:'Populations, samples, and estimates: measure a hidden town'},
 {slug:'sampling-fairly',title:'Sampling Bias and Random Assignment',desc:'Selection bias and random assignment: change who gets included'},
 {slug:'estimates-vary',title:'Sampling Distributions and the Central Limit Theorem',desc:'Sampling distributions, standard error, and the Central Limit Theorem'},
 {slug:'intervals',title:'Confidence Intervals',desc:'Confidence intervals: reveal the truth and count what covers it'},
 {slug:'testing-a-claim',title:'Hypothesis Tests and p-Values',desc:'Null models and p-values: compare suspicious results with fair coins'},
 {slug:'planning-an-experiment',title:'Experimental Design',desc:'Design a classroom experiment: controls, randomization, blocking, and replication'},
 {slug:'comparing-proportions',title:'Comparing Proportions',desc:'A/B tests, differences in proportions, and shuffling under a null model'},
 {slug:'comparing-means',title:'Comparing Means with Student’s t',desc:'Student’s t, independent groups, and paired measurements'},
 {slug:'errors-and-power',title:'Errors, Power, and Multiple Testing',desc:'False positives, power, sample size, and the cost of trying many tests'},
 {slug:'beyond-two-groups',title:'Chi-Square Tests and ANOVA',desc:'Chi-square and ANOVA: compare counts and means without testing every pair'},
 {slug:'relationships-and-prediction',title:'Correlation and Linear Regression',desc:'Correlation, regression, residuals, slope uncertainty, and prediction'},
 {slug:'reading-a-study',title:'Reading a Statistical Study',desc:'Put design, effect size, uncertainty, and practical importance together'},
];
export const chapterHref=(slug:string)=>`/reading/statistics/${slug}/`;

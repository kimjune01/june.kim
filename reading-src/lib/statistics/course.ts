/** One sequence powers the outline, progress labels, and chapter navigation. */
export const course = [
 {slug:'chance',title:'Probability and Events',desc:'Can you know the chance and still be surprised?'},
 {slug:'repeated-experiments',title:'Random Variables and Distributions',desc:'What shape appears when you repeat a chance experiment?'},
 {slug:'describing-data',title:'Center and Spread',desc:'What can an average hide?'},
 {slug:'student-surveys',title:'Descriptive Statistics and Student Surveys',desc:'What can a small student survey reveal?'},
 {slug:'samples',title:'Populations and Samples',desc:'What can a handful of observations tell us?'},
 {slug:'sampling-fairly',title:'Sampling Bias and Random Assignment',desc:'Can more data still mislead us?'},
 {slug:'estimates-vary',title:'Sampling Distributions and the Central Limit Theorem',desc:'Why do estimates move between samples?'},
 {slug:'intervals',title:'Confidence Intervals',desc:'How much uncertainty remains after sampling?'},
 {slug:'testing-a-claim',title:'Hypothesis Tests and p-Values',desc:'Could chance explain this result?'},
 {slug:'planning-an-experiment',title:'Experimental Design',desc:'What makes a comparison fair?'},
 {slug:'comparing-proportions',title:'Comparing Proportions',desc:'Did the new version help?'},
 {slug:'comparing-means',title:'Comparing Means with Student’s t',desc:'How different are these averages?'},
 {slug:'errors-and-power',title:'Errors, Power, and Multiple Testing',desc:'What might our test miss?'},
 {slug:'beyond-two-groups',title:'Chi-Square Tests and ANOVA',desc:'What changes when there are more than two groups?'},
 {slug:'relationships-and-prediction',title:'Correlation and Linear Regression',desc:'What does a fitted line tell us?'},
 {slug:'reading-a-study',title:'Reading a Statistical Study',desc:'What can this study actually claim?'},
];
export const chapterHref=(slug:string)=>`/reading/statistics/${slug}/`;

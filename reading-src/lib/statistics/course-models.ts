import jStat from 'jstat';
import {mean,median,sampleWithoutReplacement} from './inference';
import {fitLine,squaredError,type Point} from './relationships';
import type {RandomSource} from './experiments';
export const sampleVariance=(values:number[])=>values.reduce((sum,x)=>sum+(x-mean(values))**2,0)/(values.length-1);
export function fiveNumbers(values:number[]) {
  const sorted=[...values].sort((a,b)=>a-b), half=Math.floor(sorted.length/2);
  return {min:sorted[0],q1:median(sorted.slice(0,half)),median:median(sorted),q3:median(sorted.slice(Math.ceil(sorted.length/2))),max:sorted.at(-1)!};
}
export const students=Array.from({length:60},(_,id)=>{
  const mode=['Walk','Bike','Bus','Car'][id%4];
  return {id:id+1,mode,minutes:({Walk:5,Bike:10,Bus:25,Car:15}[mode]??0)+(id*7%25)};
});
export interface ABResult {a:number;b:number;n:number}
export function proportionExperiment(n:number,effect:number,random:RandomSource=Math.random):ABResult {
  const successes=(p:number)=>Array.from({length:n},()=>Number(random()<p)).reduce((a,b)=>a+b,0);
  return {a:successes(.3),b:successes(.3+effect),n};
}
export function randomizationDifferences(data:ABResult,repeats:number,random:RandomSource=Math.random) {
  const total=data.a+data.b,pool=[...Array(2*data.n-total).fill(0),...Array(total).fill(1)];
  return Array.from({length:repeats},()=>2*mean(sampleWithoutReplacement(pool,data.n,random))-total/data.n);
}
export const randomizationP=(draws:number[],observed:number)=>(1+draws.filter(x=>Math.abs(x)>=Math.abs(observed)-1e-12).length)/(draws.length+1);
export function proportionInterval({a,b,n}:ABResult) {
  if(Math.min(a,b,n-a,n-b)<10)return null;
  const effect=(b-a)/n,se=Math.sqrt((a/n*(1-a/n)+b/n*(1-b/n))/n),z=jStat.normal.inv(.975,0,1);
  return {effect,se,low:effect-z*se,high:effect+z*se};
}
function tInference(effect:number,se:number,df:number) {
  if(!(se>0))throw new RangeError('A t procedure needs positive estimated variability.');
  const t=effect/se,critical=jStat.studentt.inv(.975,df);
  return {effect,se,df,t,p:Math.min(1,2*jStat.studentt.cdf(-Math.abs(t),df)),low:effect-critical*se,high:effect+critical*se};
}
/** Direction is B minus A. Welch's method does not assume equal population variances. */
export function welchComparison(a:number[],b:number[]) {
  const va=sampleVariance(a)/a.length,vb=sampleVariance(b)/b.length;
  return tInference(mean(b)-mean(a),Math.sqrt(va+vb),(va+vb)**2/(va**2/(a.length-1)+vb**2/(b.length-1)));
}
export function pairedComparison(a:number[],b:number[]) {
  if(a.length!==b.length)throw new RangeError('A paired comparison needs one partner per observation.');
  const differences=b.map((x,i)=>x-a[i]);
  return tInference(mean(differences),Math.sqrt(sampleVariance(differences)/differences.length),differences.length-1);
}
export function normalPower(effect:number,n:number,alpha:number) {
  const se=10*Math.sqrt(2/n),cutoff=jStat.normal.inv(1-alpha/2,0,1)*se;
  return jStat.normal.cdf(-cutoff,effect,se)+jStat.normal.cdf(-cutoff,-effect,se);
}
export function powerExperiments(effect:number,n:number,alpha:number,repeats:number,random:RandomSource=Math.random) {
  const se=10*Math.sqrt(2/n),cutoff=jStat.normal.inv(1-alpha/2,0,1)*se;
  return Array.from({length:repeats},()=>{
    const z=Math.sqrt(-2*Math.log(1-random()))*Math.cos(2*Math.PI*random());
    const estimate=effect+se*z;
    return {estimate,reject:Math.abs(estimate)>=cutoff};
  });
}
/** Equal category probabilities, specified before collecting counts. */
export function chiSquareFit(counts:number[]) {
  const expected=counts.reduce((a,b)=>a+b,0)/counts.length;
  const statistic=counts.reduce((sum,count)=>sum+(count-expected)**2/expected,0),df=counts.length-1;
  return {statistic,df,expected,p:statistic===0?1:Math.max(0,1-jStat.chisquare.cdf(statistic,df))};
}
export function anova(groups:number[][]) {
  const all=groups.flat(),grand=mean(all),df1=groups.length-1,df2=all.length-groups.length;
  const between=groups.reduce((sum,g)=>sum+g.length*(mean(g)-grand)**2,0)/df1;
  const within=groups.reduce((sum,g)=>sum+g.reduce((s,x)=>s+(x-mean(g))**2,0),0)/df2;
  const statistic=between/within;
  return {statistic,df1,df2,p:statistic===0?1:Math.max(0,1-jStat.centralF.cdf(statistic,df1,df2))};
}
export function regressionInference(points:Point[]) {
  const line=fitLine(points),df=points.length-2,center=mean(points.map(p=>p.x));
  const sxx=points.reduce((sum,p)=>sum+(p.x-center)**2,0),sse=squaredError(points,line);
  const total=points.reduce((sum,p)=>sum+(p.y-mean(points.map(q=>q.y)))**2,0);
  return {...line,...tInference(line.slope,Math.sqrt(sse/df/sxx),df),rSquared:1-sse/total};
}
export const formatP=(p:number)=>p<.001?'< 0.001':p.toFixed(3);

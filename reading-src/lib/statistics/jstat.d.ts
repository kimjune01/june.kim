/** The small subset of jStat's distribution API used by these teaching activities. */
declare module 'jstat' {
  const jStat: {
    studentt: { cdf(x:number,df:number):number; inv(p:number,df:number):number };
    normal: { cdf(x:number,mean:number,sd:number):number; inv(p:number,mean:number,sd:number):number };
    chisquare: { cdf(x:number,df:number):number };
    centralF: { cdf(x:number,df1:number,df2:number):number };
  };
  export default jStat;
}

import { mean } from './inference';
/** Expected counts in 10,000 items: sensitivity 90%, false-positive rate 10%. */
export function flagCounts(defectPercent: number) {
  const defects=100*defectPercent, good=10000-defects;
  return {defectFlagged: defects*.9, defectMissed: defects*.1, goodFlagged:good*.1, goodPassed:good*.9};
}
export interface Point { x:number; y:number }
export interface Line { intercept:number; slope:number }
export function fitLine(points:Point[]):Line {
  const mx=mean(points.map(p=>p.x)), my=mean(points.map(p=>p.y));
  const slope=points.reduce((sum,p)=>sum+(p.x-mx)*(p.y-my),0)/points.reduce((sum,p)=>sum+(p.x-mx)**2,0);
  return {slope,intercept:my-slope*mx};
}
export const squaredError=(points:Point[],line:Line)=>points.reduce((sum,p)=>sum+(p.y-line.intercept-line.slope*p.x)**2,0);
export const logistic=(value:number)=>1/(1+Math.exp(-value));
export const regressionPoints:Point[]=[{x:1,y:2},{x:2,y:4},{x:3,y:3},{x:4,y:5},{x:5,y:5},{x:6,y:8},{x:7,y:7},{x:8,y:9}];

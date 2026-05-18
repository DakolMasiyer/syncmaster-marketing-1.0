import test from 'node:test';
import assert from 'node:assert/strict';
import { assignDate, getNextAvailableWeek, autoSchedule } from '../app/calendar-lib.js';

const week='2026-01-05T00:00:00.000Z';

test('assignDate returns expected ISO day offset',()=>{
  assert.equal(assignDate(week,2).slice(0,10),'2026-01-07');
  assert.equal(assignDate(week,0).slice(0,10),'2026-01-05');
});

test('getNextAvailableWeek returns same week when slots free',()=>{
  assert.equal(getNextAvailableWeek([],week).slice(0,10),'2026-01-05');
});

test('getNextAvailableWeek bumps when scheduled dates conflict',()=>{
  const existing=[{publishDate:'2026-01-07T00:00:00.000Z'}];
  assert.equal(getNextAvailableWeek(existing,week).slice(0,10),'2026-01-12');
});

test('autoSchedule maps platform days and resolves same-platform conflicts by week',()=>{
  const existing=[{publishDate:'2026-01-07T00:00:00.000Z',platform:'linkedin'}];
  const rep=[{platform:'linkedin',title:'A',content:'x'},{platform:'instagram',title:'B',content:'y'}];
  const out=autoSchedule(rep,week,existing);
  assert.equal(out[0].publishDate.slice(0,10),'2026-01-14');
  assert.equal(out[1].publishDate.slice(0,10),'2026-01-15');
  assert.equal(out[0].status,'scheduled');
});

---
layout: post
title: "Algorithm Templates: Math & Geometry"
date: 2025-10-29 00:00:00 -0700
categories: leetcode templates math geometry
permalink: /posts/2025-10-29-leetcode-templates-math-geometry/
tags: [leetcode, templates, math, geometry]
---

Minimal, copy-paste Java for combinatorics (nCk mod P) and 2D geometry primitives (cross product, point on segment).

## Contents

- [Combinatorics (nCk mod P)](#combinatorics-nck-mod-p)
- [Geometry Primitives (2D)](#geometry-primitives-2d)

## Combinatorics (nCk mod P)

```java
int MOD=1'000'000'007; int N=200000;
static long modexp(long a,long e){ long r=1%MOD; while (e > 0) { if(e 1) r=r a%MOD; a=a a%MOD; e>>=1; } return r; }
long[]fact(N+1), invfact(N+1);
static void initComb(){ fact[0]=1; for(int i=1;i<=N;++i) fact[i]=fact[i-1]*i%MOD; invfact[N]=modexp(fact[N], MOD-2); for(int i=N;i>0;--i) invfact[i-1]=invfact[i]*i%MOD; }
static long nCk(int n,int k){ if(k<0||k>n) return 0; return fact[n]*invfact[k]%MOD invfact[n-k]%MOD; }
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 62 | Unique Paths | [Link](https://leetcode.com/problems/unique-paths/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/09/24/medium-62-unique-paths/) |
| 172 | Factorial Trailing Zeroes | [Link](https://leetcode.com/problems/factorial-trailing-zeroes/) | - |

## Geometry Primitives (2D)

```java
class P{ long x,y; }
long cross(P a,P b,P c){ return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x); }
boolean onSeg(P a,P b,P c){ return Math.min(a.x,b.x)<=c.x&&c.x<=Math.max(a.x,b.x)&&Math.min(a.y,b.y)<=c.y&&c.y<=Math.max(a.y,b.y) && cross(a,b,c)==0; }
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 149 | Max Points on a Line | [Link](https://leetcode.com/problems/max-points-on-a-line/) | - |
| 223 | Rectangle Area | [Link](https://leetcode.com/problems/rectangle-area/) | - |
| 1344 | Angle Between Hands of a Clock | [Link](https://leetcode.com/problems/angle-between-hands-of-a-clock/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/04/medium-1344-angle-between-hands-of-a-clock/) |

## More templates

- **DP (counting, paths):** [Dynamic Programming](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-dp/)
- **Data structures, Graph, Search:** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/), [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/), [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)

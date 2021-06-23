; ModuleID = 'trmm_flattened_kernel.bc'
source_filename = "trmm_flattened.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local hidden void @kernel_trmm(i32 %m, i32 %n, double %alpha, [1000 x double]* %A, [1200 x double]* %B) #0 {
entry:
  %m.addr = alloca i32, align 4
  %n.addr = alloca i32, align 4
  %alpha.addr = alloca double, align 8
  %A.addr = alloca [1000 x double]*, align 8
  %B.addr = alloca [1200 x double]*, align 8
  %i = alloca i32, align 4
  %j = alloca i32, align 4
  %k = alloca i32, align 4
  %flat = alloca i32, align 4
  store i32 %m, i32* %m.addr, align 4
  store i32 %n, i32* %n.addr, align 4
  store double %alpha, double* %alpha.addr, align 8
  store [1000 x double]* %A, [1000 x double]** %A.addr, align 8
  store [1200 x double]* %B, [1200 x double]** %B.addr, align 8
  store i32 0, i32* %i, align 4
  store i32 0, i32* %j, align 4
  %0 = load i32, i32* %i, align 4
  %add = add nsw i32 %0, 1
  store i32 %add, i32* %k, align 4
  store i32 0, i32* %flat, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %1 = load i32, i32* %flat, align 4
  %conv = sitofp i32 %1 to double
  %2 = load i32, i32* %m.addr, align 4
  %conv1 = sitofp i32 %2 to double
  %mul = fmul double 5.000000e-01, %conv1
  %3 = load i32, i32* %m.addr, align 4
  %4 = load i32, i32* %n.addr, align 4
  %mul2 = mul nsw i32 %3, %4
  %5 = load i32, i32* %n.addr, align 4
  %add3 = add nsw i32 %mul2, %5
  %add4 = add nsw i32 %add3, 2
  %conv5 = sitofp i32 %add4 to double
  %mul6 = fmul double %mul, %conv5
  %cmp = fcmp olt double %conv, %mul6
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %6 = load i32, i32* %j, align 4
  %7 = load i32, i32* %n.addr, align 4
  %cmp8 = icmp slt i32 %6, %7
  br i1 %cmp8, label %if.then, label %if.else36

if.then:                                          ; preds = %for.body
  %8 = load i32, i32* %k, align 4
  %9 = load i32, i32* %m.addr, align 4
  %cmp10 = icmp slt i32 %8, %9
  br i1 %cmp10, label %if.then12, label %if.else

if.then12:                                        ; preds = %if.then
  %10 = load [1000 x double]*, [1000 x double]** %A.addr, align 8
  %11 = load i32, i32* %k, align 4
  %idxprom = sext i32 %11 to i64
  %arrayidx = getelementptr inbounds [1000 x double], [1000 x double]* %10, i64 %idxprom
  %12 = load i32, i32* %i, align 4
  %idxprom13 = sext i32 %12 to i64
  %arrayidx14 = getelementptr inbounds [1000 x double], [1000 x double]* %arrayidx, i64 0, i64 %idxprom13
  %13 = load double, double* %arrayidx14, align 8
  %14 = load [1200 x double]*, [1200 x double]** %B.addr, align 8
  %15 = load i32, i32* %k, align 4
  %idxprom15 = sext i32 %15 to i64
  %arrayidx16 = getelementptr inbounds [1200 x double], [1200 x double]* %14, i64 %idxprom15
  %16 = load i32, i32* %j, align 4
  %idxprom17 = sext i32 %16 to i64
  %arrayidx18 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx16, i64 0, i64 %idxprom17
  %17 = load double, double* %arrayidx18, align 8
  %mul19 = fmul double %13, %17
  %18 = load [1200 x double]*, [1200 x double]** %B.addr, align 8
  %19 = load i32, i32* %i, align 4
  %idxprom20 = sext i32 %19 to i64
  %arrayidx21 = getelementptr inbounds [1200 x double], [1200 x double]* %18, i64 %idxprom20
  %20 = load i32, i32* %j, align 4
  %idxprom22 = sext i32 %20 to i64
  %arrayidx23 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx21, i64 0, i64 %idxprom22
  %21 = load double, double* %arrayidx23, align 8
  %add24 = fadd double %21, %mul19
  store double %add24, double* %arrayidx23, align 8
  %22 = load i32, i32* %k, align 4
  %inc = add nsw i32 %22, 1
  store i32 %inc, i32* %k, align 4
  br label %if.end

if.else:                                          ; preds = %if.then
  %23 = load double, double* %alpha.addr, align 8
  %24 = load [1200 x double]*, [1200 x double]** %B.addr, align 8
  %25 = load i32, i32* %i, align 4
  %idxprom25 = sext i32 %25 to i64
  %arrayidx26 = getelementptr inbounds [1200 x double], [1200 x double]* %24, i64 %idxprom25
  %26 = load i32, i32* %j, align 4
  %idxprom27 = sext i32 %26 to i64
  %arrayidx28 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx26, i64 0, i64 %idxprom27
  %27 = load double, double* %arrayidx28, align 8
  %mul29 = fmul double %23, %27
  %28 = load [1200 x double]*, [1200 x double]** %B.addr, align 8
  %29 = load i32, i32* %i, align 4
  %idxprom30 = sext i32 %29 to i64
  %arrayidx31 = getelementptr inbounds [1200 x double], [1200 x double]* %28, i64 %idxprom30
  %30 = load i32, i32* %j, align 4
  %idxprom32 = sext i32 %30 to i64
  %arrayidx33 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx31, i64 0, i64 %idxprom32
  store double %mul29, double* %arrayidx33, align 8
  %31 = load i32, i32* %j, align 4
  %inc34 = add nsw i32 %31, 1
  store i32 %inc34, i32* %j, align 4
  %32 = load i32, i32* %i, align 4
  %add35 = add nsw i32 %32, 1
  store i32 %add35, i32* %k, align 4
  br label %if.end

if.end:                                           ; preds = %if.else, %if.then12
  br label %if.end39

if.else36:                                        ; preds = %for.body
  %33 = load i32, i32* %i, align 4
  %inc37 = add nsw i32 %33, 1
  store i32 %inc37, i32* %i, align 4
  store i32 0, i32* %j, align 4
  %34 = load i32, i32* %i, align 4
  %add38 = add nsw i32 %34, 1
  store i32 %add38, i32* %k, align 4
  br label %if.end39

if.end39:                                         ; preds = %if.else36, %if.end
  br label %for.inc

for.inc:                                          ; preds = %if.end39
  %35 = load i32, i32* %flat, align 4
  %inc40 = add nsw i32 %35, 1
  store i32 %inc40, i32* %flat, align 4
  br label %for.cond, !llvm.loop !2

for.end:                                          ; preds = %for.cond
  ret void
}

attributes #0 = { noinline nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 12.0.0 (https://github.com/llvm/llvm-project.git 990939c897314bd82c38d7a58c49ab9c1d209d52)"}
!2 = distinct !{!2, !3}
!3 = !{!"llvm.loop.mustprogress"}

; ModuleID = '2mm_flattened_kernel.bc'
source_filename = "2mm_flattened.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define hidden void @kernel_2mm(i32 %ni, i32 %nj, i32 %nk, i32 %nl, double %alpha, double %beta, [900 x double]* %tmp, [1100 x double]* %A, [900 x double]* %B, [1200 x double]* %C, [1200 x double]* %D) #0 {
entry:
  %ni.addr = alloca i32, align 4
  %nj.addr = alloca i32, align 4
  %nk.addr = alloca i32, align 4
  %nl.addr = alloca i32, align 4
  %alpha.addr = alloca double, align 8
  %beta.addr = alloca double, align 8
  %tmp.addr = alloca [900 x double]*, align 8
  %A.addr = alloca [1100 x double]*, align 8
  %B.addr = alloca [900 x double]*, align 8
  %C.addr = alloca [1200 x double]*, align 8
  %D.addr = alloca [1200 x double]*, align 8
  %i = alloca i32, align 4
  %j = alloca i32, align 4
  %k = alloca i32, align 4
  %dummy = alloca i32, align 4
  %i_1 = alloca i32, align 4
  %j_1 = alloca i32, align 4
  %k_1 = alloca i32, align 4
  %flat = alloca i32, align 4
  store i32 %ni, i32* %ni.addr, align 4
  store i32 %nj, i32* %nj.addr, align 4
  store i32 %nk, i32* %nk.addr, align 4
  store i32 %nl, i32* %nl.addr, align 4
  store double %alpha, double* %alpha.addr, align 8
  store double %beta, double* %beta.addr, align 8
  store [900 x double]* %tmp, [900 x double]** %tmp.addr, align 8
  store [1100 x double]* %A, [1100 x double]** %A.addr, align 8
  store [900 x double]* %B, [900 x double]** %B.addr, align 8
  store [1200 x double]* %C, [1200 x double]** %C.addr, align 8
  store [1200 x double]* %D, [1200 x double]** %D.addr, align 8
  store i32 0, i32* %dummy, align 4
  store i32 0, i32* %i, align 4
  store i32 0, i32* %j, align 4
  store i32 0, i32* %k, align 4
  store i32 0, i32* %i_1, align 4
  store i32 0, i32* %j_1, align 4
  store i32 0, i32* %k_1, align 4
  store i32 0, i32* %flat, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %0 = load i32, i32* %flat, align 4
  %1 = load i32, i32* %ni.addr, align 4
  %2 = load i32, i32* %nj.addr, align 4
  %mul = mul nsw i32 %1, %2
  %3 = load i32, i32* %nk.addr, align 4
  %mul1 = mul nsw i32 %mul, %3
  %4 = load i32, i32* %ni.addr, align 4
  %5 = load i32, i32* %nj.addr, align 4
  %mul2 = mul nsw i32 %4, %5
  %6 = load i32, i32* %nl.addr, align 4
  %mul3 = mul nsw i32 %mul2, %6
  %add = add nsw i32 %mul1, %mul3
  %7 = load i32, i32* %ni.addr, align 4
  %8 = load i32, i32* %nj.addr, align 4
  %mul4 = mul nsw i32 %7, %8
  %add5 = add nsw i32 %add, %mul4
  %9 = load i32, i32* %ni.addr, align 4
  %10 = load i32, i32* %nl.addr, align 4
  %mul6 = mul nsw i32 %9, %10
  %add7 = add nsw i32 %add5, %mul6
  %11 = load i32, i32* %ni.addr, align 4
  %mul8 = mul nsw i32 2, %11
  %add9 = add nsw i32 %add7, %mul8
  %add10 = add nsw i32 %add9, 1
  %cmp = icmp slt i32 %0, %add10
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %12 = load i32, i32* %i, align 4
  %13 = load i32, i32* %ni.addr, align 4
  %cmp11 = icmp slt i32 %12, %13
  br i1 %cmp11, label %if.then, label %if.else40

if.then:                                          ; preds = %for.body
  %14 = load i32, i32* %j, align 4
  %15 = load i32, i32* %nj.addr, align 4
  %cmp12 = icmp slt i32 %14, %15
  br i1 %cmp12, label %if.then13, label %if.else37

if.then13:                                        ; preds = %if.then
  %16 = load i32, i32* %k, align 4
  %cmp14 = icmp eq i32 %16, 0
  br i1 %cmp14, label %if.then15, label %if.end

if.then15:                                        ; preds = %if.then13
  %17 = load [900 x double]*, [900 x double]** %tmp.addr, align 8
  %18 = load i32, i32* %i, align 4
  %idxprom = sext i32 %18 to i64
  %arrayidx = getelementptr inbounds [900 x double], [900 x double]* %17, i64 %idxprom
  %19 = load i32, i32* %j, align 4
  %idxprom16 = sext i32 %19 to i64
  %arrayidx17 = getelementptr inbounds [900 x double], [900 x double]* %arrayidx, i64 0, i64 %idxprom16
  store double 0.000000e+00, double* %arrayidx17, align 8
  br label %if.end

if.end:                                           ; preds = %if.then15, %if.then13
  %20 = load i32, i32* %k, align 4
  %21 = load i32, i32* %nk.addr, align 4
  %cmp18 = icmp slt i32 %20, %21
  br i1 %cmp18, label %if.then19, label %if.else

if.then19:                                        ; preds = %if.end
  %22 = load double, double* %alpha.addr, align 8
  %23 = load [1100 x double]*, [1100 x double]** %A.addr, align 8
  %24 = load i32, i32* %i, align 4
  %idxprom20 = sext i32 %24 to i64
  %arrayidx21 = getelementptr inbounds [1100 x double], [1100 x double]* %23, i64 %idxprom20
  %25 = load i32, i32* %k, align 4
  %idxprom22 = sext i32 %25 to i64
  %arrayidx23 = getelementptr inbounds [1100 x double], [1100 x double]* %arrayidx21, i64 0, i64 %idxprom22
  %26 = load double, double* %arrayidx23, align 8
  %mul24 = fmul double %22, %26
  %27 = load [900 x double]*, [900 x double]** %B.addr, align 8
  %28 = load i32, i32* %k, align 4
  %idxprom25 = sext i32 %28 to i64
  %arrayidx26 = getelementptr inbounds [900 x double], [900 x double]* %27, i64 %idxprom25
  %29 = load i32, i32* %j, align 4
  %idxprom27 = sext i32 %29 to i64
  %arrayidx28 = getelementptr inbounds [900 x double], [900 x double]* %arrayidx26, i64 0, i64 %idxprom27
  %30 = load double, double* %arrayidx28, align 8
  %mul29 = fmul double %mul24, %30
  %31 = load [900 x double]*, [900 x double]** %tmp.addr, align 8
  %32 = load i32, i32* %i, align 4
  %idxprom30 = sext i32 %32 to i64
  %arrayidx31 = getelementptr inbounds [900 x double], [900 x double]* %31, i64 %idxprom30
  %33 = load i32, i32* %j, align 4
  %idxprom32 = sext i32 %33 to i64
  %arrayidx33 = getelementptr inbounds [900 x double], [900 x double]* %arrayidx31, i64 0, i64 %idxprom32
  %34 = load double, double* %arrayidx33, align 8
  %add34 = fadd double %34, %mul29
  store double %add34, double* %arrayidx33, align 8
  %35 = load i32, i32* %k, align 4
  %inc = add nsw i32 %35, 1
  store i32 %inc, i32* %k, align 4
  br label %if.end36

if.else:                                          ; preds = %if.end
  %36 = load i32, i32* %j, align 4
  %inc35 = add nsw i32 %36, 1
  store i32 %inc35, i32* %j, align 4
  store i32 0, i32* %k, align 4
  br label %if.end36

if.end36:                                         ; preds = %if.else, %if.then19
  br label %if.end39

if.else37:                                        ; preds = %if.then
  %37 = load i32, i32* %i, align 4
  %inc38 = add nsw i32 %37, 1
  store i32 %inc38, i32* %i, align 4
  store i32 0, i32* %j, align 4
  br label %if.end39

if.end39:                                         ; preds = %if.else37, %if.end36
  br label %if.end79

if.else40:                                        ; preds = %for.body
  %38 = load i32, i32* %i_1, align 4
  %39 = load i32, i32* %ni.addr, align 4
  %cmp41 = icmp slt i32 %38, %39
  br i1 %cmp41, label %if.then42, label %if.else76

if.then42:                                        ; preds = %if.else40
  %40 = load i32, i32* %j_1, align 4
  %41 = load i32, i32* %nl.addr, align 4
  %cmp43 = icmp slt i32 %40, %41
  br i1 %cmp43, label %if.then44, label %if.else73

if.then44:                                        ; preds = %if.then42
  %42 = load i32, i32* %k_1, align 4
  %cmp45 = icmp eq i32 %42, 0
  br i1 %cmp45, label %if.then46, label %if.end52

if.then46:                                        ; preds = %if.then44
  %43 = load double, double* %beta.addr, align 8
  %44 = load [1200 x double]*, [1200 x double]** %D.addr, align 8
  %45 = load i32, i32* %i_1, align 4
  %idxprom47 = sext i32 %45 to i64
  %arrayidx48 = getelementptr inbounds [1200 x double], [1200 x double]* %44, i64 %idxprom47
  %46 = load i32, i32* %j_1, align 4
  %idxprom49 = sext i32 %46 to i64
  %arrayidx50 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx48, i64 0, i64 %idxprom49
  %47 = load double, double* %arrayidx50, align 8
  %mul51 = fmul double %47, %43
  store double %mul51, double* %arrayidx50, align 8
  br label %if.end52

if.end52:                                         ; preds = %if.then46, %if.then44
  %48 = load i32, i32* %k_1, align 4
  %49 = load i32, i32* %nj.addr, align 4
  %cmp53 = icmp slt i32 %48, %49
  br i1 %cmp53, label %if.then54, label %if.else70

if.then54:                                        ; preds = %if.end52
  %50 = load [900 x double]*, [900 x double]** %tmp.addr, align 8
  %51 = load i32, i32* %i_1, align 4
  %idxprom55 = sext i32 %51 to i64
  %arrayidx56 = getelementptr inbounds [900 x double], [900 x double]* %50, i64 %idxprom55
  %52 = load i32, i32* %k_1, align 4
  %idxprom57 = sext i32 %52 to i64
  %arrayidx58 = getelementptr inbounds [900 x double], [900 x double]* %arrayidx56, i64 0, i64 %idxprom57
  %53 = load double, double* %arrayidx58, align 8
  %54 = load [1200 x double]*, [1200 x double]** %C.addr, align 8
  %55 = load i32, i32* %k_1, align 4
  %idxprom59 = sext i32 %55 to i64
  %arrayidx60 = getelementptr inbounds [1200 x double], [1200 x double]* %54, i64 %idxprom59
  %56 = load i32, i32* %j_1, align 4
  %idxprom61 = sext i32 %56 to i64
  %arrayidx62 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx60, i64 0, i64 %idxprom61
  %57 = load double, double* %arrayidx62, align 8
  %mul63 = fmul double %53, %57
  %58 = load [1200 x double]*, [1200 x double]** %D.addr, align 8
  %59 = load i32, i32* %i_1, align 4
  %idxprom64 = sext i32 %59 to i64
  %arrayidx65 = getelementptr inbounds [1200 x double], [1200 x double]* %58, i64 %idxprom64
  %60 = load i32, i32* %j_1, align 4
  %idxprom66 = sext i32 %60 to i64
  %arrayidx67 = getelementptr inbounds [1200 x double], [1200 x double]* %arrayidx65, i64 0, i64 %idxprom66
  %61 = load double, double* %arrayidx67, align 8
  %add68 = fadd double %61, %mul63
  store double %add68, double* %arrayidx67, align 8
  %62 = load i32, i32* %k_1, align 4
  %inc69 = add nsw i32 %62, 1
  store i32 %inc69, i32* %k_1, align 4
  br label %if.end72

if.else70:                                        ; preds = %if.end52
  %63 = load i32, i32* %j_1, align 4
  %inc71 = add nsw i32 %63, 1
  store i32 %inc71, i32* %j_1, align 4
  store i32 0, i32* %k_1, align 4
  br label %if.end72

if.end72:                                         ; preds = %if.else70, %if.then54
  br label %if.end75

if.else73:                                        ; preds = %if.then42
  %64 = load i32, i32* %i_1, align 4
  %inc74 = add nsw i32 %64, 1
  store i32 %inc74, i32* %i_1, align 4
  store i32 0, i32* %j_1, align 4
  br label %if.end75

if.end75:                                         ; preds = %if.else73, %if.end72
  br label %if.end78

if.else76:                                        ; preds = %if.else40
  %65 = load i32, i32* %dummy, align 4
  %inc77 = add nsw i32 %65, 1
  store i32 %inc77, i32* %dummy, align 4
  store i32 0, i32* %i, align 4
  store i32 0, i32* %i_1, align 4
  br label %if.end78

if.end78:                                         ; preds = %if.else76, %if.end75
  br label %if.end79

if.end79:                                         ; preds = %if.end78, %if.end39
  br label %for.inc

for.inc:                                          ; preds = %if.end79
  %66 = load i32, i32* %flat, align 4
  %inc80 = add nsw i32 %66, 1
  store i32 %inc80, i32* %flat, align 4
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

# TIME (ITERATIONS)
require(ggplot2)
require(scales)
time <- read.csv('~/probabilistic-ranking/gen/time_iterations.csv', header=F)
iter <- c(1, 2, 5, 10, 22, 46, 100, 215, 464, 1000)
colnames(time) <- c('iter', 'time1', 'time2', 'time3')
time$time1 <- time$time1 / 3600
time$time2 <- time$time2 / 3600
time$time3 <- time$time3 / 3600
# time in second step: disambiguation
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  it <- iter[i]
  means[i] <- mean(time[time$iter==it,]$time2)
  sds[i] <- sd(time[time$iter==it,]$time2)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max)
Sys.setlocale("LC_ALL", 'en_US.UTF-8')
# sampling phase
# log on x axis
ggplot(data, aes(x=iter, y=means), log10='x') + stat_function(fun=function(x) 0.02177*10**x + 0.02737, color='gray', linetype=2) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x)))
# log-log graph
ggplot(data, aes(x=iter, y=means)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x))) + scale_y_log10(breaks= trans_breaks("log10", function(x) 10^x), labels=trans_format("log10", math_format(10^.x)))

# ranking phase
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  it <- iter[i]
  means[i] <- mean(time[time$iter==it,]$time3)
  sds[i] <- sd(time[time$iter==it,]$time3)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max)
# log on x axis
ggplot(data, aes(x=iter, y=means), log10='x') + stat_function(fun=function(x) 0.0002116*10**x - 0.0038054, color='gray', linetype=2) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x)))
# log-log graph
ggplot(data, aes(x=iter, y=means), ylim=c(min(means), max(means))) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x))) + scale_y_log10(breaks= trans_breaks("log10", function(x) 10^x), labels=trans_format("log10", math_format(10^.x)))

# disambiguation phase
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  it <- iter[i]
  means[i] <- mean(time[time$iter==it,]$time1)
  sds[i] <- sd(time[time$iter==it,]$time1)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max)
# log on x axis
ggplot(data, aes(x=iter, y=means), log10='x') + ylim(0, max(ci_max)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.1) + geom_point(size=4, shape=21, fill='white') +  xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x)))

# plotting them all together
Etapa <- rep('', 30)
means <- rep(0, 30)
sds <- rep(0, 30)
n <- 10
for (i in 1:10) {
  it <- iter[i]
  Etapa[i] <- 'Desambiguação'
  means[i] <- mean(time[time$iter==it,]$time1)
  sds[i] <- sd(time[time$iter==it,]$time1)
}
for (i in 11:20) {
  it <- iter[i-10]
  Etapa[i] <- 'Amostragem de Mundos Possíveis'
  means[i] <- mean(time[time$iter==it,]$time2)
  sds[i] <- sd(time[time$iter==it,]$time2)
}
for (i in 21:30) {
  it <- iter[i-20]
  Etapa[i] <- 'Obtenção do Ranking'
  means[i] <- mean(time[time$iter==it,]$time3)
  sds[i] <- sd(time[time$iter==it,]$time3)
}
error <- qt(0.975, n-1)*sds/sqrt(n)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(iter, means, ci_min, ci_max, Etapa)
data$Etapa <- factor(data$Etapa, levels=c("Desambiguação", "Amostragem de Mundos Possíveis", "Obtenção do Ranking"))
ggplot(data, aes(x=iter, y=means, color=Etapa, group=Etapa)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=.05) + geom_line(size=0.2) + geom_point(size=2, shape=8, fill='white') + xlab('# Iterações Estocásticas') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=16), axis.title=element_text(size=16), legend.justification=c(0,1), legend.position=c(0,1), legend.key=element_blank(), legend.title=element_text(size=16), legend.text=element_text(size=16)) + scale_x_log10(breaks=10**(0:3), labels=trans_format("log10", math_format(10^.x))) + scale_y_log10(breaks= trans_breaks("log10", function(x) 10^x), labels=trans_format("log10", math_format(10^.x)))

################################################################

# TIME (INPUT_SIZE)
require(ggplot2)
require(scales)
time <- read.csv('~/probabilistic-ranking/gen/time_input.csv', header=F)
size <- c(429, 857, 1286, 1715, 2144, 2572, 3001, 3430, 3858, 4287)
colnames(time) <- c('size', 'time1', 'time2', 'time3')
time$time1 <- time$time1 / 3600
time$time2 <- time$time2 / 3600
time$time3 <- time$time3 / 3600
# time in second step: disambiguation
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  si <- size[i]
  means[i] <- mean(time[time$size==si,]$time2)
  sds[i] <- sd(time[time$size==si,]$time2)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(size, means, ci_min, ci_max)
Sys.setlocale("LC_ALL", 'en_US.UTF-8')
# sampling phase
ggplot(data, aes(x=size, y=means)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=100) + geom_point(size=4, shape=21, fill='white') +  xlab('# Referências') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14))

# ranking phase
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  si <- size[i]
  means[i] <- mean(time[time$size==si,]$time3)
  sds[i] <- sd(time[time$size==si,]$time3)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(size, means, ci_min, ci_max)
ggplot(data, aes(x=size, y=means)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=100) + geom_point(size=4, shape=21, fill='white') +  xlab('# Referências') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14))

# disambiguation phase
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  si <- size[i]
  means[i] <- mean(time[time$size==si,]$time1)
  sds[i] <- sd(time[time$size==si,]$time1)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(size, means, ci_min, ci_max)
ggplot(data, aes(x=size, y=means)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=100) + geom_point(size=4, shape=21, fill='white') +  xlab('# Referências') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=12), axis.title=element_text(size=14))

# plotting them all together
Etapa <- rep('', 30)
means <- rep(0, 30)
sds <- rep(0, 30)
n <- 10
for (i in 1:10) {
  si <- size[i]
  Etapa[i] <- 'Desambiguação'
  means[i] <- mean(time[time$size==si,]$time1)
  sds[i] <- sd(time[time$size==si,]$time1)
}
for (i in 11:20) {
  si <- size[i-10]
  Etapa[i] <- 'Amostragem de Mundos Possíveis'
  means[i] <- mean(time[time$size==si,]$time2)
  sds[i] <- sd(time[time$size==si,]$time2)
}
for (i in 21:30) {
  si <- size[i-20]
  Etapa[i] <- 'Obtenção do Ranking'
  means[i] <- mean(time[time$size==si,]$time3)
  sds[i] <- sd(time[time$size==si,]$time3)
}
error <- qt(0.975, n-1)*sds/sqrt(n)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(size, means, ci_min, ci_max, Etapa)
data$Etapa <- factor(data$Etapa, levels=c("Desambiguação", "Amostragem de Mundos Possíveis", "Obtenção do Ranking"))
ggplot(data, aes(x=size, y=means, color=Etapa, group=Etapa)) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=50) + geom_line(size=0.2) + geom_point(size=2, shape=8, fill='white') +  xlab('# Referências') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=16), axis.title=element_text(size=16), legend.justification=c(0,1), legend.position=c(0,1), legend.key=element_blank(), legend.title=element_text(size=16), legend.text=element_text(size=16))

################################################################

# TIME (TRAIN SIZE)
require(ggplot2)
require(scales)
time <- read.csv('~/probabilistic-ranking/time_train.csv', header=F)
size <- c(429, 857, 1286, 1715, 2144, 2572, 3001, 3430, 3858, 4287)
colnames(time) <- c('size', 'time')
time$time <- time$time / 3600
means <- rep(0, 10)
sds <- rep(0, 10)
for (i in 1:10) {
  si <- size[i]
  means[i] <- mean(time[time$size==si,]$time)
  sds[i] <- sd(time[time$size==si,]$time)
}
error <- qnorm(0.975)*sds/sqrt(5)
ci_min <- means - error
ci_max <- means + error
data <- data.frame(size, means, ci_min, ci_max)
Sys.setlocale("LC_ALL", 'en_US.UTF-8')
ggplot(data, aes(x=size, y=means)) + ylim(0, max(ci_max)) + geom_line(size=0.2) + geom_errorbar(aes(ymax=ci_max, ymin=ci_min), color='black', width=100) + geom_point(size=4, shape=21, fill='white') +  xlab('# Referências') + ylab('Tempo (h)') + theme_bw() + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.border=element_rect(color='black'), axis.text=element_text(size=16), axis.title=element_text(size=16))

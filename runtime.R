rm(list=ls())
library(ggplot2)
library(Cairo)

args<-commandArgs(TRUE)
inF<-args[1]
outF<-args[2]

#inF<-'/disk/pkl/Rscript/input/example.txt'
#outF<-'/disk/pkl/Rscript/output/example.png'

data<-read.table(inF,header = F,sep = '\t',stringsAsFactors = F)
colnames(data)<-c('Start','End','Type')
data$Start<-floor(data$Start/60)
data$End<-floor(data$End/60)
category<-unique(data$Type)
draw_data<-list()
for(i in 1:length(category)){
  D<-data[which(!is.na(match(data[,'Type'],category[i]))),]
  D<-D[order(D$Start),]
  maxT<-max(max(D$Start),max(D$End)) + 1
  minT<-min(min(D$Start),min(D$End))
  D_after<-data.frame(Time=rep(minT:maxT),Task=0,Type=category[i])
  for(j in 2:nrow(D_after)){
    num=0
    for(k in 1:nrow(D)){
      if((D[k,'Start']>=D_after[j-1,'Time'] && D[k,'Start']<D_after[j,'Time']) || 
         (D[k,'Start']<=D_after[j-1,'Time'] && D[k,'End']>D_after[j-1,'Time']))
        num=num+1
    }
    D_after[j,'Task']=num
  }
  if(category[i]=='bwa'||category[i]=='merge'){
    D_after$Task=D_after$Task * 12
  }
  draw_data[[i]]<-D_after
}
draw_data_1<-do.call(rbind.data.frame,draw_data)

Cairo(outF,width = 1000,height = 500)
ggplot(draw_data_1,aes(x=Time,y=Task,color=Type,group=Type)) +
  geom_line(size=1) +
  labs(x='Time(min)',y='CPU core') +
  theme_bw() +
  theme(
    panel.grid=element_line(colour=NULL, linetype = 3),
    panel.grid.major=element_line(colour="black"),
   # panel.grid.major.x=element_blank(),
    panel.grid.minor=element_blank(),
    plot.margin = unit(c(1, 1, 1, 1), "lines"),
    plot.title=element_text(hjust=0.5, face="bold",size=25),
    line=element_line(linetype=1, colour="black"),
    rect=element_rect(fill='#FFFFFF', linetype=1, colour=NA),
    axis.title = element_text(size=20,face = 'plain',color = 'black'),
    axis.text = element_text(size=18,face = 'plain',color = 'black'),
    legend.text = element_text(size=18,face = 'plain',color = 'black'),
    legend.title = element_text(size=18,face = 'plain',color = 'black'),
    legend.position="right",
    legend.direction="vertical"
  )
dev.off()
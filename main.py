import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

#miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_excel("miuul_gezinomi.xlsx")
type(df)
df.info()
df.shape
df.head()

#Kaçunique şehirvardır? Frekanslarınedir?
df["SaleCityName"].nunique()
df["SaleCityName"].value_counts()

#Kaç unique Concept vardır?
df["ConceptName"].nunique()

#Hangi Concept’den kaçar tane satış gerçekleşmiş
df["ConceptName"].value_counts()

#Şehirlere göre satışlardan toplam ne kadar kazanılmış
df.groupby("SaleCityName")["Price"].sum()

#Concept türlerine göre göre ne kadar kazanılmış
df.groupby("ConceptName")["Price"].sum()

#Şehirlere göre PRICE ortalamaları nedir
df.groupby("SaleCityName")["Price"].mean()

#Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName")["Price"].mean()

#Şehir-Concept kırılımında PRICE ortalamalarınedir?
df.groupby(["SaleCityName", "ConceptName"])["Price"].mean()

#SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
df["SaleCheckInDayDiff"] = df["SaleCheckInDayDiff"].astype("category")
df["SaleCheckInDayDiff"].dtype


# SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
# • Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullanabilirsiniz.
# • Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()], labels=["Last Minuters", "Potential Planners", "Planners", "Early Bookers"])
df.head()
df.tail()

#Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden
#inceleyiniz ?

df.groupby(["SaleCityName", "ConceptName", "EB_Score"]).agg({"Price": ["mean", "count"]}).round(2)
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]}).round(2)
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]}).round(2)



#City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).round(4).sort_values(by="Price", ascending=False)
agg_df.head(15)

#Degiskenleri kategrik yapma
agg_df.reset_index(inplace=True)
agg_df.head()

#Yeni seviye tabanlı müşterileri (persona) tanımlayınız
agg_df["Sales_level_based"] = agg_df["SaleCityName"] + "_" + agg_df["ConceptName"] + "_" + agg_df["Seasons"]


#Yeni müşterileri (personaları) segmentlere ayırınız
# Yeni personaları PRICE’a göre 4 segmente ayırınız.
# • Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız)

agg_df["Segment"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("Segment").agg({"Price": ["mean", "max", "sum"]}).round(2)

#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.

#Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
new_user = "Antalya_Herşey Dahil_High"
print(agg_df[agg_df["Sales_level_based"] == new_user])

#Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?
new_user1 = "Girne_Yarım Pansiyon_Low"
print(agg_df[agg_df["Sales_level_based"] == new_user1]["Segment"])

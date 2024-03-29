
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C

import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = pd.read_csv('Python Programing for Data Science/Kural Tabanlı Sınıflandırma/persona.csv')
df.info()
df.head()
# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df['SOURCE'].nunique()
df['SOURCE'].value_counts()

# Soru 3: Kaç unique PRICE vardır?
df['PRICE'].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df['PRICE'].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df['COUNTRY'].value_counts()



# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE":["sum"]})

# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
df['SOURCE'].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"})

#############################################
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
x = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

#############################################
# Çıktıyı PRICE'a göre sıralayınız.
#############################################

agg_df = x.sort_values(by="PRICE", ascending=False)
agg_df.head()

#############################################
# Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################

agg_df.reset_index()
agg_df


#############################################
# AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 19, 24, 31, 41, 70],
                           labels=["0_18", "19_23", "24_30", "31_40", "41_70"], right=False)
agg_df.head()

#############################################
# Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################

def combine_columns(row):
    return (row['COUNTRY'].upper() + "_" +
            row['SOURCE'].upper() + "_"  +
            row['SEX'].upper() +  "_"  +
            row['AGE_CAT'].upper())

agg_df['customer_level_based'] = agg_df.apply(combine_columns, axis=1)
agg_df.drop(['COUNTRY', 'SOURCE','SEX','AGE','AGE_CAT'], axis=1, inplace=True)
agg_df = agg_df[['customer_level_based','PRICE']]

agg_df = agg_df.groupby(['customer_level_based']).agg({"PRICE": "mean"})
agg_df.reset_index(inplace=True)
agg_df.head()


#############################################
# Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################

agg_df["SEGMENT"]= pd.qcut(agg_df['PRICE'], 4 , labels = ["D","C","B","A"])
agg_df.head()
agg_df.groupby(["SEGMENT"]).agg({"PRICE": ["mean","max","sum"]})


#############################################
# Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user2 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user2]

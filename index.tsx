/*simple react native app on expo go*/
import React, { useEffect, useState, useCallback } from "react";
import { View, Text, FlatList, ActivityIndicator, RefreshControl } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

// =============================
// CONFIG — change these values
// =============================
const API_URL = "https://o1xnv44x13.execute-api.us-east-2.amazonaws.com/basic1/getUser?user=shai";
const API_KEY = "GnxfSTv97r1ahChs079le4C3NgEfrpDFaWG1X6zG";

type RecordItem = {
  uid: number;
  user: string;
  value: number;
  flag: string;
  datetime: string;
};

export default function App() {
  const [data, setData] = useState<RecordItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setError(null);

      const headers: any = {};
      if (API_KEY) headers["x-api-key"] = API_KEY;

      const res = await fetch(API_URL, { headers });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const json = await res.json();

      const parsed = Array.isArray(json)
        ? json
        : json.body
        ? JSON.parse(json.body)
        : [];

      setData(parsed);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const getColor = (flag: string) => {
    if (flag === "HIGH") return "#ef4444";
    if (flag === "LOW") return "#f59e0b";
    return "#22c55e";
  };

  const renderItem = ({ item }: { item: RecordItem }) => (
    <View
      style={{
        backgroundColor: "white",
        borderRadius: 20,
        padding: 16,
        marginBottom: 12,
        elevation: 3,
      }}
    >
      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Text style={{ fontSize: 18, fontWeight: "bold" }}>{item.user}</Text>

        <View
          style={{
            backgroundColor: getColor(item.flag),
            paddingHorizontal: 10,
            paddingVertical: 4,
            borderRadius: 20,
          }}
        >
          <Text style={{ color: "white", fontSize: 12 }}>{item.flag}</Text>
        </View>
      </View>

      <Text style={{ fontSize: 30, fontWeight: "800", marginTop: 8 }}>
        {item.value} bpm
      </Text>

      <Text style={{ color: "gray", marginTop: 4 }}>{item.datetime}</Text>
    </View>
  );

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#f3f4f6", padding: 16 }}>
      <Text style={{ fontSize: 26, fontWeight: "bold", marginBottom: 12 }}>
        Heart Rate Dashboard
      </Text>

      {loading && <ActivityIndicator size="large" />}

      {error && (
        <Text style={{ color: "red", marginBottom: 10 }}>Error: {error}</Text>
      )}

      <FlatList
        data={data}
        keyExtractor={(item) => String(item.uid)}
        renderItem={renderItem}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      />
    </SafeAreaView>
  );
}
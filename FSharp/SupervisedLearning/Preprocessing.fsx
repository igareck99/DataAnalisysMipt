﻿#r @"..\packages\Accord.3.4.0\lib\net46\Accord.dll"
#r @"..\packages\Accord.MachineLearning.3.4.0\lib\net46\Accord.MachineLearning.dll"
#r @"..\packages\FSharp.Data.2.3.2\lib\net40\FSharp.Data.dll"
#r @"..\packages\FSharp.Charting.0.90.14\lib\net40\FSharp.Charting.dll"
#r @"bin\Debug\LibExtensions.dll"

open Accord
open Accord.MachineLearning

open FSharp.Data
open FSharp.Charting

open LibExtensions.Charting

[<Literal>]
let DataPath = __SOURCE_DIRECTORY__ + @"..\..\..\Data\preprocessing_data.csv"
type Data = CsvProvider<DataPath>
type Observation = Data.Row

let dataSet = Data.Load(DataPath)

let getNumericValues (o:Observation) =
    [o.``RFCD.Percentage.1``;
     o.``RFCD.Percentage.2``;
     o.``RFCD.Percentage.3``;
     o.``RFCD.Percentage.4``;
     o.``RFCD.Percentage.5``;
     o.``SEO.Percentage.1``;
     o.``SEO.Percentage.2``;
     o.``SEO.Percentage.3``;
     o.``SEO.Percentage.4``;
     o.``SEO.Percentage.5``;
     o.``Year.of.Birth.1``;
     o.``Number.of.Successful.Grant.1``;
     o.``Number.of.Unsuccessful.Grant.1``]

let getCategoricalValues (o:Observation) =
    [string o.``Country.of.Birth.1``;
     string o.``SEO.Code.1``;
     string o.``SEO.Code.2``;
     string o.``SEO.Code.3``;
     string o.``SEO.Code.4``;
     string o.``SEO.Code.5``;
     string o.``RFCD.Code.1``;
     string o.``RFCD.Code.2``;
     string o.``RFCD.Code.3``;
     string o.``RFCD.Code.4``;
     string o.``RFCD.Code.5``;
     string o.``A..1``;
     string o.``A.1``;
     string o.``B.1``;
     string o.``C.1``;
     string o.``No..of.Years.in.Uni.at.Time.of.Grant.1``;
     string o.``With.PHD.1``;
     string o.``Sponsor.Code``;
     string o.``Home.Language.1``;
     string o.``Person.ID.1``;
     string o.``Grant.Category.Code``;
     string o.``Faculty.No..1``;
     string o.``Role.1``;
     string o.``Dept.No..1``;
     string o.``Contract.Value.Band...see.note.A``]

let calculateMeans (rows:(float list) seq) =
    let columnsCount = (rows |> Seq.head |> List.length) - 1
    [0 .. columnsCount]
    |> List.map(fun colIdx ->
        let nonZero =
            rows
            |> Seq.map(fun row -> row.[colIdx])
            |> Seq.filter (fun col -> match col with
                            | x when nan.Equals(x) -> false
                            | x when x = 0. -> false
                            | _ -> true)
            |> Seq.toList
        let correction = nonZero |> List.max
        let colCount = nonZero |> List.length |> float
        let sum = nonZero |> List.sumBy(fun col -> col/correction)
        sum*correction/colCount)

dataSet.Rows
|> Seq.take 5
|> Seq.iter (fun o ->
    (o|>getNumericValues|>List.map string,o|>getCategoricalValues)
    ||> List.append
    |> (printfn "%A"))

let numericData = dataSet.Rows
                  |> Seq.map getNumericValues

let numericMeans = numericData |> calculateMeans
                  
let categoricalData = dataSet.Rows
                      |> Seq.map getCategoricalValues

let mapRowValues (data:float list seq) mapper =
    data
    |> Seq.map (fun values ->
        values
        |> List.mapi(fun i x -> match x with
                                | v when nan.Equals(v) -> v |> mapper i
                                | v -> v))

let mapNumericData = mapRowValues numericData

let xRealZeros = mapNumericData (fun i v -> 0.)
let xRealMean = mapNumericData (fun i v -> numericMeans.[i])
                 